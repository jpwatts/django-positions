from django.test import TestCase
from examples.nodes.models import Node
import doctest
import os
import unittest


class NodesTestCase(TestCase):
    def setUp(self):
        """
        Creates a simple tree::

            parent1
                child2
                child1
                child3
            parent2
                child4
                child5
                child6
        """
        self.parent1 = Node.objects.create(name='Parent 1')
        self.parent2 = Node.objects.create(name='Parent 2')
        self.child1 = self.parent1.children.create(name='Child 1')
        self.child2 = self.parent1.children.create(name='Child 2')
        self.child3 = self.parent1.children.create(name='Child 3')
        self.child2.position = 0
        self.child2.save()
        self.child1 = Node.objects.get(pk=self.child1.pk)
        self.child2 = Node.objects.get(pk=self.child2.pk)
        self.child3 = Node.objects.get(pk=self.child3.pk)

        self.child4 = self.parent2.children.create(name='Child 4')
        self.child5 = self.parent2.children.create(name='Child 5')
        self.child6 = self.parent2.children.create(name='Child 6')

    def tearDown(self):
        Node.objects.all().delete()

    def test_structure(self):
        """
        Tests the tree structure
        """
        result = list(Node.objects.order_by('parent__position', 'position').values_list('name', 'position'))
        expected_result = [(u'Parent 1', 0), (u'Parent 2', 1), (u'Child 2', 0), (u'Child 1', 1), (u'Child 3', 2), (u'Child 4', 0), (u'Child 5', 1), (u'Child 6', 2)]
        self.assertEqual(sorted(result), sorted(expected_result))

    def test_collection_field_change_sibling_position(self):
        """
        Set child6 as the first sibling in its branch.
        """
        self.child6.position = 0
        self.child6.save()

        result = list(Node.objects.order_by('parent__position', 'position').values_list('name', 'position'))
        expected_result = [(u'Parent 1', 0), (u'Parent 2', 1), (u'Child 2', 0), (u'Child 1', 1), (u'Child 3', 2), (u'Child 6', 0), (u'Child 4', 1), (u'Child 5', 2)]
        self.assertEqual(sorted(result), sorted(expected_result))

    def test_collection_field_change_first_child(self):
        """
        Move child2 to make it the first child of parent2
        """
        self.child2.position = 0
        self.child2.parent = Node.objects.get(pk=self.parent2.pk)
        self.child2.save()

        result = list(Node.objects.order_by('parent__position', 'position').values_list('name', 'position'))
        expected_result = [(u'Parent 1', 0), (u'Parent 2', 1), (u'Child 1', 0), (u'Child 3', 1), (u'Child 2', 0), (u'Child 4', 1), (u'Child 5', 2), (u'Child 6', 3)]
        self.assertEqual(sorted(result), sorted(expected_result))

    def test_collection_field_change_last_child(self):
        """
        Move child2 to make it the last child of parent2
        """

        self.child2.position = -1
        self.child2.parent = Node.objects.get(pk=self.parent2.pk)
        self.child2.save()

        result = list(Node.objects.order_by('parent__position', 'position').values_list('name', 'position'))
        expected_result = [(u'Parent 1', 0), (u'Parent 2', 1), (u'Child 1', 0), (u'Child 3', 1), (u'Child 4', 0), (u'Child 5', 1), (u'Child 6', 2), (u'Child 2', 3)]
        self.assertEqual(sorted(result), sorted(expected_result))

    def test_collection_field_change_sibling_1(self):
        """
        Move child2 to make it the next sibling of child4
        """

        self.child2.position = 1
        self.child2.parent = Node.objects.get(pk=self.parent2.pk)
        self.child2.save()

        result = list(Node.objects.order_by('parent__position', 'position').values_list('name', 'position'))
        expected_result = [(u'Parent 1', 0), (u'Parent 2', 1), (u'Child 1', 0), (u'Child 3', 1), (u'Child 4', 0), (u'Child 2', 1), (u'Child 5', 2), (u'Child 6', 3)]
        self.assertEqual(sorted(result), sorted(expected_result))

    def test_collection_field_change_sibling_2(self):
        """
        Move child2 to make it the next sibling of child5
        """

        self.child2.position = 2
        self.child2.parent = Node.objects.get(pk=self.parent2.pk)
        self.child2.save()

        result = list(Node.objects.order_by('parent__position', 'position').values_list('name', 'position'))
        expected_result = [(u'Parent 1', 0), (u'Parent 2', 1), (u'Child 1', 0), (u'Child 3', 1), (u'Child 4', 0), (u'Child 5', 1), (u'Child 2', 2), (u'Child 6', 3)]
        self.assertEqual(sorted(result), sorted(expected_result))

    def test_collection_field_change_sibling_3(self):
        """
        Move child2 to make it the next sibling of child6 (last child)
        """

        self.child2.position = 3
        self.child2.parent = Node.objects.get(pk=self.parent2.pk)
        self.child2.save()

        result = list(Node.objects.order_by('parent__position', 'position').values_list('name', 'position'))
        expected_result = [(u'Parent 1', 0), (u'Parent 2', 1), (u'Child 1', 0), (u'Child 3', 1), (u'Child 4', 0), (u'Child 5', 1), (u'Child 6', 2), (u'Child 2', 3)]
        self.assertEqual(sorted(result), sorted(expected_result))

    def test_deletion_1(self):
        """
        Delete child2
        """
        self.child2.delete()
        result = list(Node.objects.order_by('parent__position', 'position').values_list('name', 'position'))
        expected_result = [(u'Parent 1', 0), (u'Parent 2', 1), (u'Child 1', 0), (u'Child 3', 1), (u'Child 4', 0), (u'Child 5', 1), (u'Child 6', 2)]
        self.assertEqual(sorted(result), sorted(expected_result))

    def test_deletion_2(self):
        """
        Delete child3
        """
        self.child3.delete()
        result = list(Node.objects.order_by('parent__position', 'position').values_list('name', 'position'))
        expected_result = [(u'Parent 1', 0), (u'Parent 2', 1), (u'Child 2', 0), (u'Child 1', 1), (u'Child 4', 0), (u'Child 5', 1), (u'Child 6', 2)]
        self.assertEqual(sorted(result), sorted(expected_result))

    def test_deletion_3(self):
        """
        Delete child1
        """
        self.child1.delete()
        result = list(Node.objects.order_by('parent__position', 'position').values_list('name', 'position'))
        expected_result = [(u'Parent 1', 0), (u'Parent 2', 1), (u'Child 2', 0), (u'Child 3', 1), (u'Child 4', 0), (u'Child 5', 1), (u'Child 6', 2)]
        self.assertEqual(sorted(result), sorted(expected_result))

    def test_deletion_4(self):
        """
        Delete parent1
        """
        self.parent1.delete()
        result = list(Node.objects.order_by('parent__position', 'position').values_list('name', 'position'))
        expected_result = [(u'Parent 2', 0), (u'Child 4', 0), (u'Child 5', 1), (u'Child 6', 2)]
        self.assertEqual(sorted(result), sorted(expected_result))


class ReorderTestCase(TestCase):
    def tearDown(self):
        Node.objects.all().delete()

    @unittest.skip("Not sure if this should fail or not. Skipping until there is time to figure it out.")
    def test_assigning_parent(self):
        a = Node.objects.create(name=u"A")
        b = Node.objects.create(name=u"B")
        c = Node.objects.create(name=u"C")
        self.assertEqual(a.position, 0)
        self.assertEqual(b.position, 1)
        self.assertEqual(c.position, 2)
        b.parent = a
        b.save()
        # A hasn't changed.
        self.assertEqual(a.position, 0)
        # B has been positioned relative to A.
        self.assertEqual(b.position, 0)
        # C has moved up to fill the gap left by B.
        self.assertEqual(c.position, 1)

    @unittest.skip("Not sure if this should fail or not. Skipping until there is time to figure it out.")
    def test_changing_parent(self):
        a = Node.objects.create(name=u"A")
        b = Node.objects.create(name=u"B")
        c = Node.objects.create(name=u"C", parent=a)
        d = Node.objects.create(name=u"D", parent=a)
        self.assertEqual(a.parent, None)
        self.assertEqual(a.position, 0)
        self.assertEqual(b.parent, None)
        self.assertEqual(b.position, 1)
        self.assertEqual(c.parent, a)
        self.assertEqual(c.position, 0)
        self.assertEqual(d.parent, a)
        self.assertEqual(d.position, 1)
        c.parent = b
        c.save()
        # A's position hasn't changed.
        self.assertEqual(a.parent, None)
        self.assertEqual(a.position, 0)
        # B's position hasn't changed.
        self.assertEqual(b.parent, None)
        self.assertEqual(b.position, 1)
        # C's relative position hasn't changed.
        self.assertEqual(c.parent, b)
        self.assertEqual(c.position, 0)
        # D has moved up to fill the gap left by C.
        self.assertEqual(d.parent, a)
        self.assertEqual(d.position, 0)


def suite():
    s = unittest.TestSuite()
    s.addTest(unittest.TestLoader().loadTestsFromTestCase(NodesTestCase))
    s.addTest(doctest.DocFileSuite(os.path.join('doctests', 'nodes.txt'), optionflags=doctest.REPORT_ONLY_FIRST_FAILURE))
    return s
