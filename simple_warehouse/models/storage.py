from odoo import models, fields, api, tools, _


class WTItem(models.Model):
    _name = 'simple_warehouse.item'

    name = fields.Char(string=_('Name'))
    serial_no = fields.Char(string=_('Serial number'))
    document_ids = fields.One2many(comodel_name="simple_warehouse.item_documents", inverse_name="item_id")
    category_id = fields.Many2one('simple_warehouse.item_categories', string=_('Category'))
    notes = fields.Text('Notes')
    photos_ids = fields.One2many('simple_warehouse.item_images', 'item_id')

    # Item images
    image = fields.Binary("Image", attachment=True, compute='compute_images')
    image_medium = fields.Binary("Medium-sized image", attachment=True)
    image_small = fields.Binary("Small-sized image", attachment=True, compute='compute_images')

    # TODO: Expendable flag for future reference. Once project status implementation is completed,
    # used inventory should be returned to either a selected warehouse, or the one inventory was taken
    # from in the first place, except for items with this flag. Expendable items should disappear.
    expendable = fields.Boolean(string=_('Expendable'))

    quantity_ids = fields.One2many(comodel_name='simple_warehouse.quantity', inverse_name='item_id',
                                   domain=[('warehouse_id', '!=', None)])

    items_quants = fields.Text(string="Quantity", compute='_get_items_quantity')

    def _get_items_quantity(self):
        for one in self:
            warehouses_and_quants = ''
            for one_quantity in one.quantity_ids:
                warehouses_and_quants += one_quantity.warehouse_id.name + ' - ' + str(one_quantity.amount) + ', \n'
            one.items_quants = warehouses_and_quants

    @api.one
    @api.depends('image_medium')
    def compute_images(self):
        resized_images = tools.image_get_resized_images(self.image_medium, return_big=True,
                                                        avoid_resize_medium=False)
        self.image_medium = resized_images['image_medium']
        self.image_small = resized_images['image_small']
        self.image = resized_images['image']

class WTItemImages(models.Model):
    _name = 'simple_warehouse.item_images'

    name = fields.Char(string='Filename')
    image = fields.Binary(string=_('Image'))
    comment = fields.Text(string=_('Notes'))

    item_id = fields.Many2one('simple_warehouse.item')

class ItemDocuments(models.Model):
    _name = 'simple_warehouse.item_documents'
    name = fields.Char(string=_("Document"), required=True)
    document_name = fields.Char(string=_("Filename"), required=True)
    document = fields.Binary(string=_("Document"), required=True)
    item_id = fields.Many2one(comodel_name='simple_warehouse.item', required=True)

class ItemCategories(models.Model):
    _name = 'simple_warehouse.item_categories'
    name = fields.Char(string=_("Category Name"), required=True)

    items_ids = fields.One2many('simple_warehouse.item', 'category_id', string=_('Items'))

class WTQuantity(models.Model):
    _name = 'simple_warehouse.quantity'

    name = fields.Char(string=_('Name'), compute='set_name')
    item_id = fields.Many2one(comodel_name='simple_warehouse.item', string=_('Item'), required=True)
    amount = fields.Integer(string=_('Amount'), required=True)
    inventory_id = fields.Many2one(comodel_name='simple_warehouse.inventory', string=_('Inventory'), ondelete="cascade")
    warehouse_id = fields.Many2one(comodel_name='simple_warehouse.warehouse', string=_('Warehouse'),
                                   compute='set_warehouse_id', store=True)

    @api.depends('item_id', 'amount')
    def set_name(self):
        for record in self:
            if record.item_id and record.amount:
                record.name = record.item_id.name + ' : ' + str(record.amount)

    @api.depends('inventory_id')
    def set_warehouse_id(self):
        for record in self:
            if not record.warehouse_id:
                warehouse_id = self.env['simple_warehouse.warehouse'].search(
                    [('inventory_id', '=', record.inventory_id.id)]).id
                record.warehouse_id = warehouse_id

    # While it does consolidate on creation, it would probably be a good idea to write
    # a method which goes through records and consolidate doubles if they do happen to exist
    @api.model
    def create(self, vals):
        same_item = self.search(
            [('item_id', '=', vals.get('item_id', False)), ('inventory_id', '=', vals.get('inventory_id', False))])
        if same_item:
            total_amount = same_item[0].amount + vals.get('amount', 0)
            vals.update({'amount': total_amount})
            same_item[0].write(vals)
            return same_item[0]
        else:
            return super(WTQuantity, self).create(vals)


class WTInventory(models.Model):
    _name = 'simple_warehouse.inventory'

    quantity_ids = fields.One2many(comodel_name='simple_warehouse.quantity', inverse_name='inventory_id', string=_('Items'))


class WTWarehouse(models.Model):
    _name = 'simple_warehouse.warehouse'
    _inherits = {'simple_warehouse.inventory': 'inventory_id'}

    name = fields.Char(string=_('Name'), required=True)
    inventory_id = fields.Many2one(comodel_name='simple_warehouse.inventory', ondelete='cascade')
    reservation_ids = fields.One2many(comodel_name='simple_warehouse.transfer', inverse_name='reserved_location_id')

    def unlink(self):
        self.inventory_id.unlink()
        return super(WTWarehouse, self).unlink()


class WTTransfer(models.Model):
    _name = 'simple_warehouse.transfer'
    _inherits = {'simple_warehouse.inventory': 'inventory_id'}

    source_location_id = fields.Many2one(comodel_name='simple_warehouse.warehouse', string=_('Source location'))
    target_location_id = fields.Many2one(comodel_name='simple_warehouse.warehouse', string=_('Target location'))
    reserved_location_id = fields.Many2one(comodel_name='simple_warehouse.warehouse', string=_('Reserved location'))
    inventory_id = fields.Many2one(comodel_name='simple_warehouse.inventory', ondelete='cascade')

    state = fields.Selection([
        ('waiting', "Waiting for availability"),
        ('available', "Available"),
        ('reserved', "Reserved"),
        ('done', "Done"),
    ])

    # Not sure whether this is a good solution to preventing picking of the same warehouse
    # It's not symmetrical, but if you make it symmetrical it can get annoying
    # I'll make it symmetrical for now..
    @api.onchange('source_location_id', 'target_location_id')
    def location_onchange(self):
        domain = {}
        domain['domain'] = {'source_location_id': [('id', '!=', self.target_location_id.id)],
                            'target_location_id': [('id', '!=', self.source_location_id.id)]}
        return domain

    def action_wait(self):
        self.state = 'waiting'

    def action_available(self):
        self.state = 'available'

    def action_reserve(self):
        self.reserved_location_id = self.source_location_id
        self.state = 'reserved'

    def action_transfer(self):
        source_inventory_id = self.source_location_id.inventory_id.id
        target_inventory_id = self.target_location_id.inventory_id.id
        for quantity in self.quantity_ids:
            item_id = quantity.item_id.id
            amount = quantity.amount
            # Remove from source inventory
            source_quantity = self.env['simple_warehouse.quantity'].search(
                [('item_id', '=', item_id), ('inventory_id', '=', source_inventory_id)])
            remaining_amount = source_quantity[0].amount - amount
            # Handle cases when no stock remains
            if remaining_amount == 0:
                source_quantity.unlink()
            else:
                source_quantity.write({'amount': remaining_amount})
            # Add to target inventory
            transfer_quantity = {'item_id': item_id, 'amount': amount, 'inventory_id': target_inventory_id}
            self.env['simple_warehouse.quantity'].create(transfer_quantity)
            # Remove reservation
            self.reserved_location_id = None
        self.state = 'done'

    def check_availability(self):
        available = False
        for record in self:
            warehouse = record.source_location_id
            for quantity in record.inventory_id.quantity_ids:
                item_id = quantity.item_id.id
                reservation_ids = warehouse.reservation_ids
                available_amount = self.env['simple_warehouse.quantity'].search(
                    [('item_id', '=', item_id), ('inventory_id', '=', warehouse.inventory_id.id)]).amount
                reserved_amount = 0
                for reservation in reservation_ids:
                    reserved_quantity = self.env['simple_warehouse.quantity'].search(
                        [('item_id', '=', item_id), ('inventory_id', '=', reservation.reserved_location_id.id)])
                    reserved_amount += reserved_quantity.amount
                if available_amount < reserved_amount + quantity.amount:
                    return False
                else:
                    available = True
        return available

    def unlink(self):
        self.inventory_id.unlink()
        return super(WTTransfer, self).unlink()
