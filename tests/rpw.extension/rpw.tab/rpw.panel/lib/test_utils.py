from rpw import revit, DB
doc = revit.doc

def delete_all_walls():
    collector = DB.FilteredElementCollector(doc)
    walls = collector.OfClass(DB.Wall).ToElements()
    if walls:
        t = DB.Transaction(doc, 'Delete Walls')
        t.Start()
        for wall in walls:
            doc.Delete(wall.Id)
        t.Commit()

def make_wall():
    collector = DB.FilteredElementCollector(doc)
    level = collector.OfClass(DB.Level).FirstElement()
    pt1 = DB.XYZ(0, 0, 0)
    pt2 = DB.XYZ(20, 20, 0)
    wall_line = DB.Line.CreateBound(pt1, pt2)

    t = DB.Transaction(doc, 'Add Wall')
    t.Start()
    wall = DB.Wall.Create(doc, wall_line, level.Id, False)
    t.Commit()
    return wall
