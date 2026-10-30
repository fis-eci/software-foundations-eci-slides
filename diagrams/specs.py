"""
specs.py — every diagram of Unidad 5 (Diseño con Astah).

    python diagrams/specs.py                 # writes diagrams/out/*.svg
    python diagrams/specs.py --wiki <dir>    # also copies light SVGs to the wiki

Conventions (same as the Astah models students deliver):
  * MYSD — conceptual: «I» identifier, «U» unique, / derived, [m..n] multiplicity.
           Colours = Grandes Conceptos: k1 Clientes, k2 Bienes, k3 Facturas.
  * DOPO — '*' prefix marks members added in the current version, '_' static.
"""

import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from uml import Diagram, Sequence, standalone  # noqa: E402

D = {}


def reg(d):
    D[d.name] = d
    return d


# ===========================================================================
# MYSD · Empresa comercializadora
# ===========================================================================

def mysd_general():
    d = reg(Diagram('mysd-conceptos-general', 900, 380, 'Diseño conceptual general: grandes conceptos'))
    d.tag(60, 40, 'Ciclo 1 · Ventas', 'k1').tag(600, 40, 'Ciclo 2 · Compras', 'k3')
    d.cls('Cliente', 60, 90, tone='k1', w=150)
    d.cls('Factura', 340, 90, tone='k1', w=150)
    d.cls('Bien', 340, 260, tone='k2', w=150)
    d.cls('Proveedor', 640, 90, tone='k3', w=150)
    d.cls('Compra', 640, 260, tone='k3', w=150)
    d.edge('Cliente', 'Factura', ma='1', mb='*', label='EsDueño', arrow='>')
    d.edge('Factura', 'Bien', ma='*', mb='1..*', label='Vende', arrow='>', loff=(28, 0))
    d.edge('Compra', 'Bien', ma='*', mb='1..*', label='Adquiere', arrow='<')
    d.edge('Compra', 'Proveedor', ma='*', mb='1', label='SeHaceA', arrow='>', loff=(40, 0))
    d.edge('Proveedor', 'Bien', ma='*', mb='*', label='Ofrece', arrow='>', lpos=.42, loff=(-28, -6))
    d.text(450, 360, 'Grandes conceptos (GC): Clientes · Bienes · Facturas | Proveedores · Compras', 'u-label', 'middle')


def mysd_conceptos(name='mysd-conceptos-ventas', tags=False):
    d = reg(Diagram(name, 960, 640, 'Diseño conceptual extendido · Ciclo Ventas'))
    d.cls('Cliente', 40, 30, tone='k1', attrs=[
        '«I» tid : TipoId', '«I» nid : Entero(15)', 'nombre : Cadena(20)',
        '«U» correo : Cadena(10)[0..1]', 'telefonos : Cadena(10)[1..*]'])
    d.cls('Factura', 600, 40, tone='k3', attrs=['numero : Consecutivo', 'fecha : Fecha', '/ total : Moneda'])
    d.cls('LineaFactura', 600, 250, tone='k3', attrs=['cantidad : Cantidad', 'precioVenta : Moneda'])
    d.cls('Bien', 110, 260, tone='k2', attrs=['«I» codigo : Cadena(5)', 'nombre : Cadena(10)', 'precioVenta : Moneda'])
    d.cls('Servicio', 30, 440, tone='k2', attrs=['manoDeObra : Moneda', '/ costo : Moneda'])
    d.cls('Producto', 420, 440, tone='k2', attrs=['existencias : Cantidad', 'precioCompra : Moneda'])
    d.cls('Utiliza', 250, 560, tone='k2', attrs=['unidades : Cantidad'], compact=True)
    d.edge('Cliente', 'Factura', ma='1', mb='*', label='EsDueño', arrow='>', lpos=.55)
    d.edge('Cliente', 'Cliente', via=[(90, 205), (230, 205)], ma='*', mb='0..1', label='Recomienda', arrow='<', loff=(0, 18))
    d.edge('Factura', 'LineaFactura', kind='comp', ma='1', mb='1..*')
    d.edge('LineaFactura', 'Bien', ma='*', mb='1', label='EsDe', arrow='<')
    d.edge('Servicio', 'Bien', kind='gen', via=[(115, 410), (210, 410)])
    d.edge('Producto', 'Bien', kind='gen', via=[(520, 410), (210, 410)])
    d.edge('Servicio', 'Producto', ma='*', mb='*', label='Utiliza', arrow='>', aclass='Utiliza', loff=(0, -8))
    d.edge('Producto', 'Producto', via=[(660, 462), (660, 500)], ma='*', mb='*', label='PuedeReemplazar', arrow='>', loff=(64, 0))
    if tags:
        d.tag(40, 4, 'Clientes', 'k1').tag(312, 124, 'Telefonos', 'k1')
        d.tag(600, 14, 'Facturas', 'k3').tag(600, 224, 'LineasFactura', 'k3')
        d.tag(110, 234, 'Bienes', 'k2').tag(30, 414, 'Servicios', 'k2').tag(420, 414, 'Productos', 'k2')
        d.tag(400, 596, 'Utilizaciones', 'k2').tag(680, 530, 'Reemplazos', 'k2')
        d.tag(245, 196, 'FK en Clientes', 'k4').tag(380, 64, 'FK en Facturas', 'k4').tag(440, 300, 'FK en LineasFactura', 'k4')
        d.tag(690, 194, 'FK en LineasFactura', 'k4')
    return d


def mysd_funciones():
    d = reg(Diagram('mysd-funciones', 780, 340, 'Diagrama de funciones · Ciclo Ventas'))
    d.actor('gv', 80, 40, 'Gerente de ventas').actor('pr', 700, 40, 'Proveedor')
    d.actor('ve', 80, 210, 'Vendedor').actor('cl', 700, 210, 'Cliente')
    d.usecase('mb', 315, 40, 'Mantener Bien', tone='k2')
    d.usecase('mc', 315, 175, 'Mantener Cliente', tone='k1')
    d.usecase('rf', 315, 265, 'Registrar Factura', tone='k3')
    for a, u in [('gv', 'mb'), ('pr', 'mb'), ('ve', 'mc'), ('cl', 'mc'), ('ve', 'rf'), ('cl', 'rf')]:
        d.edge(a, u)


def mysd_mini():
    d = reg(Diagram('mysd-modelo-mini', 1290, 560, 'Diseño lógico · Modelo Mini'))
    d.cls('Clientes', 60, 20, tone='k1', compact=True, attrs=[
        'PK    tid : CHAR(2)', 'PK    nid : NUMBER(15)', '      nombre : VARCHAR(20)',
        'UK    correo : VARCHAR(10)', 'FK    tidRecomienda : CHAR(2)', 'FK    nidRecomienda : NUMBER(15)'])
    d.cls('Telefonos', 60, 300, tone='k1', compact=True, attrs=[
        'PK FK tid : CHAR(2)', 'PK FK nid : NUMBER(15)', 'PK    telefono : VARCHAR(10)'])
    d.cls('Facturas', 400, 20, tone='k3', compact=True, attrs=[
        'PK    numero : NUMBER(9)', '      fecha : DATE', '      total : NUMBER(10,2)',
        'FK    tidCliente : CHAR(2)', 'FK    nidCliente : NUMBER(15)'])
    d.cls('LineasFactura', 400, 300, tone='k3', compact=True, attrs=[
        'PK FK factura : NUMBER(9)', 'PK FK bien : VARCHAR(5)', '      cantidad : NUMBER(5)', '      precioVenta : NUMBER(10,2)'])
    d.cls('Bienes', 720, 300, tone='k2', compact=True, attrs=[
        'PK    codigo : VARCHAR(5)', '      nombre : VARCHAR(10)', '      precioVenta : NUMBER(10,2)'])
    d.cls('Servicios', 720, 450, tone='k2', compact=True, attrs=['PK FK codigo : VARCHAR(5)', '      manoDeObra : NUMBER(10,2)'])
    d.cls('Productos', 720, 110, tone='k2', compact=True, attrs=[
        'PK FK codigo : VARCHAR(5)', '      existencias : NUMBER(5)', '      precioCompra : NUMBER(10,2)'])
    d.cls('Utilizaciones', 1030, 300, tone='k2', compact=True, attrs=[
        'PK FK servicio : VARCHAR(5)', 'PK FK producto : VARCHAR(5)', '      unidades : NUMBER(5)'])
    d.cls('Reemplazos', 1030, 110, tone='k2', compact=True, attrs=[
        'PK FK producto : VARCHAR(5)', 'PK FK reemplazo : VARCHAR(5)'])
    d.edge('Telefonos', 'Clientes', kind='fk')
    d.edge('Clientes', 'Clientes', kind='fk', via=[(36, 120), (36, 150)])
    d.edge('Facturas', 'Clientes', kind='fk')
    d.edge('LineasFactura', 'Facturas', kind='fk')
    d.edge('LineasFactura', 'Bienes', kind='fk')
    d.edge('Servicios', 'Bienes', kind='fk')
    d.edge('Productos', 'Bienes', kind='fk')
    d.edge('Utilizaciones', 'Servicios', kind='fk', via=[(1140, 488)])
    d.edge('Utilizaciones', 'Productos', kind='fk', via=[(1000, 330), (1000, 170)])
    d.edge('Reemplazos', 'Productos', kind='fk', da=(0, -14), db=(0, -14))
    d.edge('Reemplazos', 'Productos', kind='fk', da=(0, 14), db=(0, 14))
    d.text(60, 545, 'PK clave primaria · UK clave única · FK clave foránea (la flecha apunta a la tabla referenciada)', 'u-label')


def mysd_fisico():
    d = reg(Diagram('mysd-componentes-actores', 1080, 470, 'Diseño físico · Componentes y actores'))
    d.actor('ve', 70, 70, 'Vendedor').actor('gv', 70, 300, 'Gerente de ventas')
    d.cls('PA_VENDEDOR', 200, 30, stereo='actor PL/SQL', tone='k4', compact=True, ops=[
        '+ ad_cliente(...)', '+ mo_cliente(...)', '+ el_cliente(xTid, xNid)',
        '+ ad_factura(xTid, xNid)', '+ ad_linea(xNumero, xBien, xCant)', '+ co_servicio(xCodigo)'])
    d.cls('PA_GERENTE_VENTAS', 200, 280, stereo='actor PL/SQL', tone='k4', compact=True, ops=[
        '+ ad_producto(...)', '+ ad_servicio(...)', '+ mo_bien(...)', '+ el_bien(xCodigo)', '+ co_bienes()'])
    d.cls('PC_CLIENTES', 640, 10, stereo='componente PL/SQL', tone='k1', compact=True, ops=[
        '+ ad_cliente(xTid, xNid, xNombre, xCorreo, xTel)', '+ ad_telefono(xTid, xNid, xTel)',
        '+ mo_cliente(xTid, xNid, xNombre, xCorreo)', '+ el_cliente(xTid, xNid)'])
    d.cls('PC_FACTURAS', 640, 170, stereo='componente PL/SQL', tone='k3', compact=True, ops=[
        '+ ad_factura(xTid, xNid) : NUMBER', '+ ad_linea(xNumero, xBien, xCantidad)', '+ co_factura(xNumero) : SYS_REFCURSOR'])
    d.cls('PC_BIENES', 640, 315, stereo='componente PL/SQL', tone='k2', compact=True, ops=[
        '+ ad_producto(xCodigo, xNombre, xPrecio, xCompra)', '+ ad_servicio(xCodigo, xNombre, xPrecio, xMano)',
        '+ mo_bien(xCodigo, xNombre, xPrecio)', '+ el_bien(xCodigo)',
        '+ co_servicio(xCodigo) : SYS_REFCURSOR', '+ co_bienes : SYS_REFCURSOR'])
    d.edge('ve', 'PA_VENDEDOR')
    d.edge('gv', 'PA_GERENTE_VENTAS')
    d.edge('PA_VENDEDOR', 'PC_CLIENTES', kind='dep', label='usa', lpos=.5)
    d.edge('PA_VENDEDOR', 'PC_FACTURAS', kind='dep')
    d.edge('PA_VENDEDOR', 'PC_BIENES', kind='dep', da=(60, 0))
    d.edge('PA_GERENTE_VENTAS', 'PC_BIENES', kind='dep', label='usa')


# ===========================================================================
# DOPO · Batalla naval
# ===========================================================================

def dopo_paquetes():
    d = reg(Diagram('dopo-paquetes', 700, 260, 'Diagrama de paquetes · Batalla N'))
    d.package('presentation', 20, 50, 220, 170, 'presentation', tone='k4',
              body='<text class="u-mem" x="44" y="140">BatallaNavalGUI</text>')
    d.package('domain', 380, 50, 300, 170, 'domain', tone='k1',
              body=''.join('<text class="u-mem" x="%d" y="%d">%s</text>' % (x, y, t) for x, y, t in [
                  (404, 96, 'Tablero'), (404, 122, 'Flota'), (404, 148, 'PortaAviones'), (404, 174, 'Barco'),
                  (560, 96, 'Avion'), (560, 122, 'Marino'), (560, 148, 'Posicion')]))
    d.edge('presentation', 'domain', kind='dep', label='«use»')


def dopo_presentacion():
    d = reg(Diagram('dopo-presentacion', 720, 330, 'Diagrama de clases · presentation'))
    d.cls('JFrame', 70, 10, stereo='javax.swing', tone='n', compact=True)
    d.cls('BatallaNavalGUI', 20, 110, tone='k4', attrs=[
        '- tablero : Tablero', '- panelTablero : JPanel', '- botonAtacar : JButton'], ops=[
        '+ BatallaNavalGUI()', '- prepareElements() : void', '- prepareActions() : void',
        '- refresh() : void', '_+ main(args : String[]) : void'])
    d.cls('Tablero', 440, 150, name='domain::Tablero', tone='k1', compact=True)
    d.edge('BatallaNavalGUI', 'JFrame', kind='gen')
    d.edge('BatallaNavalGUI', 'Tablero', kind='nav', rb='tablero', mb='1')
    d.note(400, 230, 'La presentación solo conoce al Tablero:\ntoda la lógica vive en domain.', w=300)


def dopo_dominio(name='dopo-dominio-v1', version=1):
    """version 1 = inicial (TT1) · 2 = Ciclo 1 (atributos) · 3 = Ciclo 2 · 4 = final (Ciclos 3 y 4)."""
    d = reg(Diagram(name, 1200, 700, 'Diagrama de clases · domain · versión %d' % version))

    def mark(lines, since):
        """'*' marks members new in `since`; older ones lose the mark."""
        return [l if version == since else l.replace('*', '') for l in lines]

    t_attrs, t_ops, f_attrs, f_ops = [], [], ['- nombre : String'], []
    crew = lambda n: []
    statics = []
    pa_ops, b_ops, av_ops, pos_ops = [], [], [], []
    if version >= 2:
        t_attrs = mark(['*_+ MINIMO : int = -100 {readOnly}', '*_+ MAXIMO : int = 100 {readOnly}'], 2)
        f_attrs += mark(['*- codigo : String {readOnly}'], 2)
        f_ops = mark(['*+ getCodigo() : String'], 2)
        crew = lambda n: mark(['*_+ TRIPULANTES : int = %d {readOnly}' % n, '*_- puntaje : int'], 2)
        statics = mark(['*_+ getPuntaje() : int', '*_+ setPuntaje(puntaje : int) : void'], 2)
        pa_ops, b_ops, av_ops = list(statics), list(statics), list(statics)
    if version >= 3:
        t_ops = mark(['*+ flotasLlamadas(nombre : String) : int'], 3)
        f_ops = ['+ getNombre() : String'] + f_ops + mark([
            '*+ numeroMaquinas() : int', '*+ suficientesMarinos() : boolean', '*+ alias() : int',
            '*+ disponibilidadEnPortaaviones() : int', '*+ muevase(dLon : int, dLat : int) : void'], 3)
        pa_ops += mark(['*+ disponibilidad() : int'], 3)
        b_ops += mark(['*+ muevase(dLon : int, dLat : int) : void'], 3)
        pos_ops += mark(['*+ muevase(dLon : int, dLat : int) : void'], 3)
    if version >= 4:
        t_ops += ['*+ enemigas(flota : Flota) : ArrayList<Flota>']
        f_ops += ['*+ seranDestruidas(lon : int, lat : int) : ArrayList<Object>',
                  '*+ esBuenAtaque(lon : int, lat : int) : boolean',
                  '*+ enAire() : ArrayList<String>', '*+ placasEnAire() : ArrayList<String>',
                  '*+ problemaEnAire() : boolean']
        pa_ops += ['*+ esta(lon : int, lat : int) : boolean']
        b_ops += ['*+ esta(lon : int, lat : int) : boolean']
        av_ops += ['*+ isEnAire() : boolean', '*+ getPlaca() : String', '*+ esta(lon : int, lat : int) : boolean']
        pos_ops += ['*+ esta(lon : int, lat : int) : boolean']

    d.cls('Tablero', 30, 20, tone='k1', attrs=t_attrs, ops=t_ops)
    T = d.nodes['Tablero']
    d.cls('Flota', 30, T[1] + T[3] + 90, tone='k1', attrs=f_attrs, ops=f_ops)
    F = d.nodes['Flota']
    col = max(T[0] + T[2], F[0] + F[2]) + 150
    d.cls('Posicion', col, 20, tone='n', attrs=['- longitud : int', '- latitud : int'], ops=pos_ops)
    PO = d.nodes['Posicion']
    d.cls('Avion', col, PO[1] + PO[3] + 60, tone='k2', attrs=['- placa : String', '- enAire : boolean'] + crew(2), ops=av_ops)
    A = d.nodes['Avion']
    d.cls('PortaAviones', col, A[1] + A[3] + 60, tone='k2', attrs=['- numero : int', '- capacidad : int'] + crew(5), ops=pa_ops)
    P = d.nodes['PortaAviones']
    d.cls('Barco', col, P[1] + P[3] + 60, tone='k2', attrs=['- numero : int'] + crew(4), ops=b_ops)
    B = d.nodes['Barco']
    right = max(A[0] + A[2], P[0] + P[2], B[0] + B[2], PO[0] + PO[2])
    d.cls('Marino', right + 170, P[1] + 10, tone='k3', attrs=['- nombre : String', '- rango : int'])
    M = d.nodes['Marino']

    d.edge('Tablero', 'Flota', ra='tablero', rb='flotas', mb='*', da=(-T[2] / 2 + 50, 0), db=(-F[2] / 2 + 50, 0))
    d.edge('Flota', 'Avion', kind='nav', rb='aviones', mb='*', da=(0, -12))
    d.edge('Flota', 'PortaAviones', kind='nav', rb='portaAviones', mb='*')
    d.edge('Flota', 'Barco', kind='nav', rb='barcos', mb='*', da=(0, 12))
    low = max(B[1] + B[3], F[1] + F[3], M[1] + M[3]) + 40
    d.edge('Flota', 'Marino', kind='nav', rb='marinos', mb='*', via=[(F[0] + 70, low), (M[0] + M[2] / 2, low)])
    d.edge('PortaAviones', 'Avion', kind='nav', rb='aviones', mb='*', via=[(A[0] + A[2] - 40, P[1] - 30)],
           db=(0, 0))
    d.edge('Avion', 'Posicion', kind='nav', rb='ubicacion', mb='1', da=(0, 0))
    d.edge('PortaAviones', 'Posicion', kind='nav', rb='ubicacion', mb='1',
           via=[(col - 30, P[1] + 22), (col - 30, PO[1] + 25)])
    d.edge('Barco', 'Posicion', kind='nav', rb='ubicacion', mb='1',
           via=[(col - 55, B[1] + 22), (col - 55, PO[1] + 50)])
    d.edge('Avion', 'Marino', kind='nav', rb='piloto', mb='1',
           via=[(right + 70, A[1] + 30), (right + 70, M[1] + 22)])
    d.edge('Avion', 'Marino', kind='nav', rb='copiloto', mb='0..1',
           via=[(M[0] + M[2] / 2, A[1] + 55)])
    d.edge('PortaAviones', 'Marino', kind='nav', rb='marinos', mb='*', da=(0, 10), db=(0, 10))
    d.edge('Barco', 'Marino', kind='nav', rb='marinos', mb='*',
           via=[(M[0] + M[2] + 30, B[1] + 25), (M[0] + M[2] + 30, M[1] + 40)])
    d.w = int(M[0] + M[2] + 90)
    d.h = int(low + 30)
    return d


def dopo_memoria():
    d = reg(Diagram('dopo-memoria', 1260, 640, 'Mapa de memoria · Ciclo 1'))
    d.cls('tablero', 520, 10, name='tablero : Tablero', underline=True, compact=True, tone='k1',
          attrs=['flotas = [f1, f2]'])
    d.cls('f1', 120, 120, name='f1 : Flota', underline=True, compact=True, tone='k1', attrs=[
        'nombre = "LA GRAN FLOTA BLANCA"', 'aviones = [hr100, jb100]', 'portaAviones = [pa100]',
        'barcos = []', 'marinos = [sperry, henry, john]', 'tablero = tablero'])
    d.cls('f2', 760, 120, name='f2 : Flota', underline=True, compact=True, tone='k1', attrs=[
        'nombre = "LA GRAN ARMADA DE CASTILLA"', 'aviones = [peace]', 'portaAviones = []',
        'barcos = [b900]', 'marinos = [pedrarias, fernando]', 'tablero = tablero'])
    d.cls('pa100', 20, 330, name='pa100 : PortaAviones', underline=True, compact=True, tone='k2', attrs=[
        'numero = 100', 'capacidad = 4', 'ubicacion = null', 'aviones = [hr100, jb100]', 'marinos = [sperry]'])
    d.cls('hr100', 290, 330, name='hr100 : Avion', underline=True, compact=True, tone='k2', attrs=[
        'placa = "HR100"', 'enAire = true', 'ubicacion = null', 'piloto = henry', 'copiloto = null'])
    d.cls('jb100', 490, 330, name='jb100 : Avion', underline=True, compact=True, tone='k2', attrs=[
        'placa = "JB100"', 'enAire = true', 'ubicacion = null', 'piloto = john', 'copiloto = null'])
    d.cls('b900', 790, 330, name='b900 : Barco', underline=True, compact=True, tone='k2', attrs=[
        'numero = 900', 'ubicacion = null', 'marinos = [pedrarias]'])
    d.cls('peace', 1030, 330, name='peace : Avion', underline=True, compact=True, tone='k5', attrs=[
        'placa = "PEACE"', 'enAire = false', 'ubicacion = null', 'piloto = null', 'copiloto = null'])
    d.cls('sperry', 20, 520, name='sperry : Marino', underline=True, compact=True, tone='k3', attrs=['nombre = "Sperry"', 'rango = 0'])
    d.cls('henry', 230, 520, name='henry : Marino', underline=True, compact=True, tone='k3', attrs=['nombre = "Henry Reuterdahl"', 'rango = 0'])
    d.cls('john', 470, 520, name='john : Marino', underline=True, compact=True, tone='k3', attrs=['nombre = "John Charles Roach"', 'rango = 0'])
    d.cls('pedrarias', 760, 520, name='pedrarias : Marino', underline=True, compact=True, tone='k3', attrs=['nombre = "Pedrarias Dávila"', 'rango = 0'])
    d.cls('fernando', 1010, 520, name='fernando : Marino', underline=True, compact=True, tone='k3', attrs=['nombre = "Fernando Villamil"', 'rango = 0'])
    for row in [('tablero', 'f1', 'flotas[0]'), ('tablero', 'f2', 'flotas[1]', True),
                    ('f1', 'pa100', 'portaAviones[0]'), ('f1', 'hr100', 'aviones[0]'), ('f1', 'jb100', 'aviones[1]', True),
                    ('f2', 'b900', 'barcos[0]'), ('f2', 'peace', 'aviones[0]'),
                    ('pa100', 'hr100', 'aviones'), ('pa100', 'sperry', 'marinos[0]'),
                    ('hr100', 'henry', 'piloto'), ('jb100', 'john', 'piloto'), ('b900', 'pedrarias', 'marinos[0]')]:
        a, b, r, *fl = row
        d.edge(a, b, kind='nav', rb=r, flip=bool(fl and fl[0]))
    d.edge('f2', 'fernando', kind='nav', rb='marinos[1]', via=[(1200, 250)])
    d.text(20, 630, 'Cada lista es un objeto ArrayList: se muestra su contenido. rango = 0 indica que el valor no se especifica (valor por defecto).', 'u-label')
    d.h = 650


# ----- Sequence diagrams ----------------------------------------------------

def dopo_secuencias():
    S = Sequence
    reg(S('seq-numeroMaquinas', [('f', ':Flota'), ('av', 'aviones:ArrayList'), ('pa', 'portaAviones:ArrayList'), ('b', 'barcos:ArrayList')], [
        ('msg', 'f', 'av', 'size()'), ('ret', 'av', 'f', 'nAviones'),
        ('msg', 'f', 'pa', 'size()'), ('ret', 'pa', 'f', 'nPortaAviones'),
        ('msg', 'f', 'b', 'size()'), ('ret', 'b', 'f', 'nBarcos'),
        ('note', 'f', 'return nAviones + nPortaAviones + nBarcos'),
    ], col=180, title='Flota.numeroMaquinas()'))
    reg(S('seq-suficientesMarinos', [('f', ':Flota'), ('pa', 'portaAviones:ArrayList'), ('b', 'barcos:ArrayList'), ('av', 'aviones:ArrayList'), ('m', 'marinos:ArrayList')], [
        ('msg', 'f', 'pa', 'size()'), ('ret', 'pa', 'f', 'nP'),
        ('msg', 'f', 'b', 'size()'), ('ret', 'b', 'f', 'nB'),
        ('msg', 'f', 'av', 'size()'), ('ret', 'av', 'f', 'nA'),
        ('note', 'f', 'requeridos = nP*PortaAviones.TRIPULANTES + nB*Barco.TRIPULANTES + nA*Avion.TRIPULANTES'),
        ('msg', 'f', 'm', 'size()'), ('ret', 'm', 'f', 'disponibles'),
        ('note', 'f', 'return disponibles >= requeridos'),
    ], col=165, w=900, title='Flota.suficientesMarinos()'))
    reg(S('seq-alias', [('f', ':Flota'), ('t', 'tablero:Tablero'), ('o', 'otra:Flota')], [
        ('msg', 'f', 't', 'flotasLlamadas(nombre)'),
        ('frag', 'loop', 'otra : flotas', ['t', 'o'], [
            ('msg', 't', 'o', 'getNombre()'), ('ret', 'o', 't', 'nombreOtra'),
            ('frag', 'opt', 'nombreOtra.equals(nombre)', ['t'], [('self', 't', 'n++')])]),
        ('ret', 't', 'f', 'n'),
        ('note', 'f', 'return n - 1   // sin contarse a sí misma'),
    ], col=230, title='Flota.alias()'))
    reg(S('seq-disponibilidad', [('f', ':Flota'), ('p', 'p:PortaAviones'), ('a', 'aviones:ArrayList')], [
        ('frag', 'loop', 'p : portaAviones', ['f', 'a'], [
            ('msg', 'f', 'p', 'disponibilidad()'),
            ('msg', 'p', 'a', 'size()'), ('ret', 'a', 'p', 'cargados'),
            ('ret', 'p', 'f', 'capacidad - cargados'),
            ('self', 'f', 'total += disponibles')]),
        ('note', 'f', 'return total'),
    ], col=230, title='Flota.disponibilidadEnPortaaviones()'))
    reg(S('seq-muevase', [('f', ':Flota'), ('b', 'b:Barco'), ('u', 'ubicacion:Posicion')], [
        ('frag', 'loop', 'b : barcos', ['f', 'u'], [
            ('msg', 'f', 'b', 'muevase(dLon, dLat)'),
            ('msg', 'b', 'u', 'muevase(dLon, dLat)'),
            ('frag', 'opt', 'nueva posición dentro de [MINIMO, MAXIMO]', ['u'], [
                ('self', 'u', 'longitud += dLon; latitud += dLat')])]),
    ], col=230, w=820, title='Flota.muevase(dLon, dLat)'))
    reg(S('seq-seranDestruidas', [('f', ':Flota'), ('p', 'p:PortaAviones'), ('b', 'b:Barco'), ('a', 'a:Avion')], [
        ('frag', 'loop', 'p : portaAviones', ['f', 'p'], [
            ('msg', 'f', 'p', 'esta(lon, lat)'), ('ret', 'p', 'f', 'afectado'),
            ('self', 'f', '[afectado] destruidas.add(p)')]),
        ('frag', 'loop', 'b : barcos', ['f', 'b'], [
            ('msg', 'f', 'b', 'esta(lon, lat)'), ('ret', 'b', 'f', 'afectado'),
            ('self', 'f', '[afectado] destruidas.add(b)')]),
        ('frag', 'loop', 'a : aviones', ['f', 'a'], [
            ('msg', 'f', 'a', 'isEnAire()'), ('ret', 'a', 'f', 'vuela'),
            ('msg', 'f', 'a', '[!vuela] esta(lon, lat)'), ('ret', 'a', 'f', 'afectado'),
            ('self', 'f', '[!vuela && afectado] destruidas.add(a)')]),
        ('note', 'f', 'return destruidas'),
    ], col=190, w=760, title='Flota.seranDestruidas(lon, lat)'))
    reg(S('seq-esta', [('b', ':Barco'), ('u', 'ubicacion:Posicion')], [
        ('frag', 'opt', 'ubicacion != null', ['b', 'u'], [
            ('msg', 'b', 'u', 'esta(lon, lat)'),
            ('ret', 'u', 'b', 'longitud == lon && latitud == lat')]),
        ('note', 'b', 'return resultado (false si no tiene ubicación)'),
    ], col=300, w=560, title='Barco.esta(lon, lat)'))
    reg(S('seq-esBuenAtaque', [('f', ':Flota'), ('t', 'tablero:Tablero'), ('e', 'enemiga:Flota')], [
        ('self', 'f', 'propias = seranDestruidas(lon, lat)'),
        ('msg', 'f', 't', 'enemigas(this)'), ('ret', 't', 'f', 'enemigas'),
        ('frag', 'loop', 'enemiga : enemigas', ['f', 'e'], [
            ('msg', 'f', 'e', 'seranDestruidas(lon, lat)'), ('ret', 'e', 'f', 'destruidas'),
            ('self', 'f', 'afectadas += destruidas.size()')]),
        ('note', 'f', 'return propias.isEmpty() && afectadas > 0'),
    ], col=240, w=820, title='Flota.esBuenAtaque(lon, lat)'))
    reg(S('seq-enAire', [('f', ':Flota'), ('t', 'tablero:Tablero'), ('e', 'enemiga:Flota'), ('a', 'a:Avion')], [
        ('msg', 'f', 't', 'enemigas(this)'), ('ret', 't', 'f', 'enemigas'),
        ('frag', 'loop', 'enemiga : enemigas', ['f', 'a'], [
            ('msg', 'f', 'e', 'placasEnAire()'),
            ('frag', 'loop', 'a : aviones', ['e', 'a'], [
                ('msg', 'e', 'a', 'isEnAire()'), ('ret', 'a', 'e', 'vuela'),
                ('frag', 'opt', 'vuela', ['e', 'a'], [
                    ('msg', 'e', 'a', 'getPlaca()'), ('ret', 'a', 'e', 'placa'),
                    ('self', 'e', 'placas.add(placa)')])]),
            ('ret', 'e', 'f', 'placasEnemiga'),
            ('self', 'f', 'placas.addAll(placasEnemiga)')]),
        ('note', 'f', 'return placas'),
    ], col=210, w=860, title='Flota.enAire()'))
    reg(S('seq-problemaEnAire', [('f', ':Flota'), ('en', 'enemigos:ArrayList')], [
        ('self', 'f', 'enemigos = enAire()'),
        ('self', 'f', 'propias = placasEnAire()'),
        ('frag', 'loop', 'placa : propias', ['f', 'en'], [
            ('msg', 'f', 'en', 'contains(placa)'), ('ret', 'en', 'f', 'repetida'),
            ('frag', 'opt', 'repetida', ['f'], [('note', 'f', 'return true')])]),
        ('note', 'f', 'return false'),
    ], col=320, w=640, title='Flota.problemaEnAire()'))


def build_all():
    mysd_general()
    mysd_conceptos()
    mysd_conceptos('mysd-bosquejo-logico', tags=True)
    mysd_funciones()
    mysd_mini()
    mysd_fisico()
    dopo_paquetes()
    dopo_presentacion()
    dopo_dominio('dopo-dominio-v1', 1)
    dopo_dominio('dopo-dominio-v2', 2)
    dopo_dominio('dopo-dominio-v3', 3)
    dopo_dominio('dopo-dominio-v4', 4)
    dopo_memoria()
    dopo_secuencias()


if __name__ == '__main__':
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, 'out')
    os.makedirs(out, exist_ok=True)
    build_all()
    for name, d in D.items():
        m = d.markup()
        with open(os.path.join(out, name + '.frag.svg'), 'w', encoding='utf-8', newline='\n') as f:
            f.write(m)
        with open(os.path.join(out, name + '.svg'), 'w', encoding='utf-8', newline='\n') as f:
            f.write(standalone(m))
    print('%d diagrams written to %s' % (len(D), out))
    if '--wiki' in sys.argv:
        dest = sys.argv[sys.argv.index('--wiki') + 1]
        os.makedirs(dest, exist_ok=True)
        for name in D:
            shutil.copy(os.path.join(out, name + '.svg'), os.path.join(dest, name + '.svg'))
        print('Copied light SVGs to', dest)
