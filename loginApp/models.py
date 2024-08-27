# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Cajas(models.Model):
    id_caja = models.AutoField(primary_key=True)
    dni = models.ForeignKey('Empleados', models.DO_NOTHING, db_column='DNI')  # Field name made lowercase.
    estado_caja = models.CharField(max_length=15)
    fechaaperturacaja = models.DateTimeField(db_column='FechaAperturaCaja')  # Field name made lowercase.
    fechacierrecaja = models.DateTimeField(db_column='FechaCierreCaja')  # Field name made lowercase.
    total_ingresos_caja = models.DecimalField(db_column='Total_ingresos_Caja', max_digits=10, decimal_places=2)  # Field name made lowercase.
    total_egresos_caja = models.DecimalField(db_column='Total_Egresos_Caja', max_digits=10, decimal_places=2)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'cajas'


class Clientes(models.Model):
    id_clientes = models.AutoField(db_column='ID_Clientes', primary_key=True)  # Field name made lowercase.
    nombre_cli = models.CharField(db_column='Nombre_Cli', max_length=50, blank=True, null=True)  # Field name made lowercase.
    apellido_cli = models.CharField(db_column='Apellido_Cli', max_length=50, blank=True, null=True)  # Field name made lowercase.
    dni = models.CharField(db_column='DNI', max_length=10, blank=True, null=True)  # Field name made lowercase.
    telefono = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'clientes'


class Compras(models.Model):
    id_compra = models.AutoField(primary_key=True)
    id_provxprod = models.ForeignKey('Provxprod', models.DO_NOTHING, db_column='id_provxprod')
    id_caja = models.ForeignKey(Cajas, models.DO_NOTHING, db_column='id_caja')
    cantidad = models.IntegerField()
    precio_total = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_compra = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'compras'


class DetalleCompras(models.Model):
    id_det_compra = models.AutoField(primary_key=True)
    id_compra = models.ForeignKey(Compras, models.DO_NOTHING, db_column='id_compra')
    id_factura = models.ForeignKey('Facturas', models.DO_NOTHING, db_column='id_Factura')  # Field name made lowercase.
    cant_prod_comp = models.IntegerField()
    subtotal = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'detalle_compras'


class DetalleVentas(models.Model):
    id_det_venta = models.AutoField(primary_key=True)
    id_venta = models.ForeignKey('Ventas', models.DO_NOTHING, db_column='id_venta')
    id_factura = models.ForeignKey('Facturas', models.DO_NOTHING, db_column='id_Factura')  # Field name made lowercase.
    id_prod = models.ForeignKey('Productos', models.DO_NOTHING, db_column='ID_Prod')  # Field name made lowercase.
    cant_prod_vendido = models.IntegerField()
    subtotal = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'detalle_ventas'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Empleados(models.Model):
    dni = models.AutoField(db_column='DNI', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=50)  # Field name made lowercase.
    apellido = models.CharField(db_column='Apellido', max_length=50)  # Field name made lowercase.
    edad = models.IntegerField(db_column='Edad', blank=True, null=True)  # Field name made lowercase.
    telefono = models.CharField(max_length=20, blank=True, null=True)
    correo = models.CharField(max_length=50)
    direccion = models.CharField(max_length=60, blank=True, null=True)
    id_user = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='id_user')

    class Meta:
        managed = False
        db_table = 'empleados'


class Facturas(models.Model):
    id_factura = models.AutoField(db_column='id_Factura', primary_key=True)  # Field name made lowercase.
    id_clientes = models.ForeignKey(Clientes, models.DO_NOTHING, db_column='ID_Clientes')  # Field name made lowercase.
    total = models.DecimalField(max_digits=7, decimal_places=2)
    descuento = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    metodo_pago = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'facturas'


class Productos(models.Model):
    id_productos = models.AutoField(db_column='ID_Productos', primary_key=True)  # Field name made lowercase.
    tipo_prod = models.CharField(db_column='Tipo_Prod', max_length=50, blank=True, null=True)  # Field name made lowercase.
    talle_prod = models.CharField(db_column='Talle_Prod', max_length=7, blank=True, null=True)  # Field name made lowercase.
    color_prod = models.CharField(db_column='Color_Prod', max_length=30, blank=True, null=True)  # Field name made lowercase.
    genero_prod = models.CharField(db_column='Genero_Prod', max_length=30, blank=True, null=True)  # Field name made lowercase.
    precio_unitario_venta = models.FloatField(db_column='Precio_unitario_venta', blank=True, null=True)  # Field name made lowercase.
    descripcion = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'productos'


class Proveedores(models.Model):
    id_proveedores = models.AutoField(db_column='ID_Proveedores', primary_key=True)  # Field name made lowercase.
    nombre_prov = models.CharField(db_column='Nombre_Prov', max_length=50)  # Field name made lowercase.
    tipo_prov = models.CharField(db_column='Tipo_Prov', max_length=50)  # Field name made lowercase.
    correo_prov = models.CharField(db_column='Correo_Prov', max_length=60, blank=True, null=True)  # Field name made lowercase.
    telefono = models.CharField(max_length=20)
    direccion = models.CharField(db_column='Direccion', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'proveedores'


class Provxprod(models.Model):
    id_provxprod = models.AutoField(db_column='Id_ProvXProd', primary_key=True)  # Field name made lowercase.
    id_prov_pxp = models.ForeignKey(Proveedores, models.DO_NOTHING, db_column='ID_Prov_pxp')  # Field name made lowercase.
    id_prod_pxp = models.ForeignKey(Productos, models.DO_NOTHING, db_column='ID_Prod_pxp')  # Field name made lowercase.
    descripcion = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'provxprod'


class Stock(models.Model):
    id_stock = models.AutoField(primary_key=True)
    id_prod = models.ForeignKey(Productos, models.DO_NOTHING, db_column='ID_Prod')  # Field name made lowercase.
    stock_min = models.IntegerField(blank=True, null=True)
    stock_actual = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stock'


class Ventas(models.Model):
    id_venta = models.AutoField(db_column='Id_Venta', primary_key=True)  # Field name made lowercase.
    id_caja = models.ForeignKey(Cajas, models.DO_NOTHING, db_column='id_caja')
    fecha_venta = models.DateTimeField()
    descripcion_venta_realizada = models.CharField(max_length=254, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ventas'
