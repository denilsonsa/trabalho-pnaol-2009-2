import bpy
import Blender
import random
import sys

Blender.Window.EditMode(0)

bola_mesh = None
iteration = []
bola = []

def new_ball(raio, name="Bola"):
    global bola_mesh
    # Creating the actual object that contains the mesh
    scn = bpy.data.scenes.active
    obj = scn.objects.new(bola_mesh, name)

    obj.setSize(raio,raio,raio)

    # Adding IPO curve for the color
    #obj.setIpo(new_ipo_color(name))

    obj.getData(mesh=1).materials = [new_ball_material(name)]
    # Setting the default Material for this ball
    #mesh.materials = [bola_material]
    # Too bad the following lines don't work...
    #mesh.setMaterials([bola_material])
    #obj.setMaterials([bola_material])


    # Adding a subsurf modifier (just to make it even prettier)
    subsurf = obj.modifiers.append(Blender.Modifier.Types.SUBSURF)

    subsurf[Blender.Modifier.Settings.RENDER] = 1
    subsurf[Blender.Modifier.Settings.REALTIME] = 0
    subsurf[Blender.Modifier.Settings.EDITMODE] = 0

    subsurf[Blender.Modifier.Settings.LEVELS] = 1
    subsurf[Blender.Modifier.Settings.RENDLEVELS] = 1

    return obj


def new_ball_material(name="Bola"):
    mat = Blender.Material.New(name+"Mat")
    mat.R = random.random()
    mat.G = random.random()
    mat.B = random.random()
    return mat


def new_ball_mesh():
    global bola_material
    # Creating the mesh
    mesh = Blender.Mesh.Primitives.UVsphere(16,16,2)
    mesh.name = "BolaMesh"

    # Setting smooth rendering
    for f in mesh.faces:
        f.smooth = True

    return mesh


def new_bezier_point(x, y, knot_len=1):
    # Note: the knot_len is completely ignored when handleTypes are set to AUTO,
    # i.e., Blender will calculate new positions for the handles automatically.
    b = Blender.BezTriple.New( (
        x-knot_len, y, 0,
        x, y, 0,
        x+knot_len, y, 0,
    ) )
    # Bezier handle types:
    # http://wiki.blender.org/index.php/Doc:Manual/Modelling/Curves#B.C3.A9ziers
    b.handleTypes = [
        Blender.BezTriple.HandleTypes["AUTO"],
        Blender.BezTriple.HandleTypes["AUTO"],
    ]
    return b


def array(points):
    "Função usada dentro do execfile() ao ler o arquivo 'points.txt'."
    global iteration
    iteration.append(points)


def main():
    global bola_mesh, iteration

    bola_mesh = new_ball_mesh()

    execfile("points.txt", globals())

    scaling = 100.0

    for i in range(numbolas):
        bola.append( new_ball(
            raio[i]/scaling,
            name = "Bola%03d" % (i+1,)
        ))

    it = iteration[0]
    for i,coords in enumerate(it[1:]):
        bola[i].setLocation(
            coords[0]/scaling,
            coords[1]/scaling,
            coords[2]/scaling
        )

    Blender.Redraw()


if __name__ == "__main__":
    main()
