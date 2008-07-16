from positions.examples.nodes.models import Node


tests = """

# create some parent nodes

>>> Node.objects.create(name='Parent 1')
<Node: Parent 1>

>>> Node.objects.order_by('position').values_list('name', 'position')
[(u'Parent 1', 0)]

>>> Node.objects.create(name='Parent 2')
<Node: Parent 2>

>>> Node.objects.order_by('position').values_list('name', 'position')
[(u'Parent 1', 0), (u'Parent 2', 1)]

>>> parent3 = Node.objects.create(name='Parent 3', position=0)

>>> Node.objects.order_by('position').values_list('name', 'position')
[(u'Parent 3', 0), (u'Parent 1', 1), (u'Parent 2', 2)]

>>> parent3.position = 999
>>> parent3.save()

>>> Node.objects.order_by('position').values_list('name', 'position')
[(u'Parent 1', 0), (u'Parent 2', 1), (u'Parent 3', 2)]

>>> parent3.position = -2
>>> parent3.save()

>>> Node.objects.order_by('position').values_list('name', 'position')
[(u'Parent 1', 0), (u'Parent 3', 1), (u'Parent 2', 2)]

>>> parent3.delete()

>>> Node.objects.order_by('position').values_list('name', 'position')
[(u'Parent 1', 0), (u'Parent 2', 1)]


# create some children

>>> parent1 = Node.objects.order_by('position')[0]
>>> parent1
<Node: Parent 1>

>>> parent1.children.create(name='Child 1')
<Node: Child 1>

>>> Node.objects.order_by('parent__position', 'position').values_list('name', 'position')
[(u'Parent 1', 0), (u'Parent 2', 1), (u'Child 1', 0)]

>>> child2 = parent1.children.create(name='Child 2')

>>> Node.objects.order_by('parent__position', 'position').values_list('name', 'position')
[(u'Parent 1', 0), (u'Parent 2', 1), (u'Child 1', 0), (u'Child 2', 1)]

>>> child2.position = 0
>>> child2.save()

>>> Node.objects.order_by('parent__position', 'position').values_list('name', 'position')
[(u'Parent 1', 0), (u'Parent 2', 1), (u'Child 2', 0), (u'Child 1', 1)]

>>> parent2 = Node.objects.filter(parent__isnull=True).order_by('position')[1]
>>> parent2
<Node: Parent 2>

>>> parent2.children.create(name='Child 3')
<Node: Child 3>

>>> Node.objects.order_by('parent__position', 'position').values_list('name', 'position')
[(u'Parent 1', 0), (u'Parent 2', 1), (u'Child 2', 0), (u'Child 1', 1), (u'Child 3', 0)]

"""


__test__ = {'tests': tests}
