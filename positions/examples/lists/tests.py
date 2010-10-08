from positions.examples.lists.models import List, Item


tests = """
>>> l = List.objects.create(name='To Do')


# create a couple items using the default position

>>> l.items.create(name='Write Tests')
<Item: Write Tests>

>>> l.items.values_list('name', 'position')
[(u'Write Tests', 0)]

>>> l.items.create(name='Excersize')
<Item: Excersize>

>>> l.items.values_list('name', 'position').order_by('position')
[(u'Write Tests', 0), (u'Excersize', 1)]


# create an item with an explicit position

>>> l.items.create(name='Learn to spell Exercise', position=0)
<Item: Learn to spell Exercise>

>>> l.items.values_list('name', 'position').order_by('position')
[(u'Learn to spell Exercise', 0), (u'Write Tests', 1), (u'Excersize', 2)]


# save an item without changing it's position

>>> excersize = l.items.order_by('-position')[0]
>>> excersize.name = 'Exercise'
>>> excersize.save()

>>> l.items.values_list('name', 'position').order_by('position')
[(u'Learn to spell Exercise', 0), (u'Write Tests', 1), (u'Exercise', 2)]


# delete an item

>>> learn_to_spell = l.items.order_by('position')[0]
>>> learn_to_spell.delete()

>>> l.items.values_list('name', 'position').order_by('position')
[(u'Write Tests', 0), (u'Exercise', 1)]


# create a couple more items

>>> l.items.create(name='Drink less Coke')
<Item: Drink less Coke>

>>> l.items.create(name='Go to Bed')
<Item: Go to Bed>

>>> l.items.values_list('name', 'position').order_by('position')
[(u'Write Tests', 0), (u'Exercise', 1), (u'Drink less Coke', 2), (u'Go to Bed', 3)]


# move item to end using None

>>> write_tests = l.items.order_by('position')[0]
>>> write_tests.position = None
>>> write_tests.save()

>>> l.items.values_list('name', 'position').order_by('position')
[(u'Exercise', 0), (u'Drink less Coke', 1), (u'Go to Bed', 2), (u'Write Tests', 3)]


# move item using negative index

>>> write_tests.position = -3
>>> write_tests.save()

>>> l.items.values_list('name', 'position').order_by('position')
[(u'Exercise', 0), (u'Write Tests', 1), (u'Drink less Coke', 2), (u'Go to Bed', 3)]


# move item to position

>>> write_tests.position = 2
>>> write_tests.save()

>>> l.items.values_list('name', 'position').order_by('position')
[(u'Exercise', 0), (u'Drink less Coke', 1), (u'Write Tests', 2), (u'Go to Bed', 3)]


# move item to beginning

>>> sleep = l.items.order_by('-position')[0]
>>> sleep.position = 0
>>> sleep.save()

>>> l.items.values_list('name', 'position').order_by('position')
[(u'Go to Bed', 0), (u'Exercise', 1), (u'Drink less Coke', 2), (u'Write Tests', 3)]


# check auto_now updates

>>> sleep_updated, excersize_updated, eat_better_updated, write_tests_updated = [i.updated for i in l.items.order_by('position')]
>>> eat_better = l.items.order_by('-position')[1]
>>> eat_better.position = 1
>>> eat_better.save()
>>> todo_list = list(l.items.order_by('position'))

>>> sleep_updated == todo_list[0].updated
True

>>> eat_better_updated < todo_list[1].updated
True

>>> excersize_updated < todo_list[2].updated
True

>>> write_tests_updated == excersize_updated
True


# create an item using negative index
# http://github.com/jpwatts/django-positions/issues/#issue/5

>>> l.items.values_list('name', 'position').order_by('position')
[(u'Go to Bed', 0), (u'Drink less Coke', 1), (u'Exercise', 2), (u'Write Tests', 3)]

>>> fix_issue_5 = Item(list=l, name="Fix Issue #5")
>>> fix_issue_5.position
-1

>>> fix_issue_5.position = -2
>>> fix_issue_5.position
-2

>>> fix_issue_5.save()
>>> fix_issue_5.position
3

>>> l.items.values_list('name', 'position').order_by('position')
[(u'Go to Bed', 0), (u'Drink less Coke', 1), (u'Exercise', 2), (u'Fix Issue #5', 3), (u'Write Tests', 4)]

# Try again, now that the model has been saved.
>>> fix_issue_5.position = -2
>>> fix_issue_5.save()
>>> fix_issue_5.position
3

>>> l.items.values_list('name', 'position').order_by('position')
[(u'Go to Bed', 0), (u'Drink less Coke', 1), (u'Exercise', 2), (u'Fix Issue #5', 3), (u'Write Tests', 4)]


# create an item using with a position of zero
http://github.com/jpwatts/django-positions/issues#issue/7

>>> item0 = l.items.create(name="Fix Issue #7", position=0)
>>> item0.position
0

>>> l.items.values_list('name', 'position').order_by('position')
[(u'Fix Issue #7', 0), (u'Go to Bed', 1), (u'Drink less Coke', 2), (u'Exercise', 3), (u'Fix Issue #5', 4), (u'Write Tests', 5)]

"""


__test__ = {'tests': tests}
