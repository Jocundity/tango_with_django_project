from django.test import TestCase
from rango.models import Page, Category
from django.urls import reverse
from datetime import timedelta
from django.utils import timezone

# Create your tests here.

class CategoryMethodTests(TestCase):
    def test_ensure_views_are_positive(self):
        """
        Ensures the number of views received for a Category are positive of zero.
        """

        category = add_category("test", 1, 0)
        
        self.assertEqual((category.views >= 0), True)

    def test_slug_line_creation(self):
        """
        Checks to make sure that when a category is created,
        an appropriate slug is created.
        Example: "Random Category String" should be "random-category-string"
        """

        category = add_category("Random Category String")

        self.assertEqual(category.slug, 'random-category-string')

class ImdexViewTests(TestCase):
    def test_index_view_with_no_categories(self):
        """
        If no categories exist, the appropriate message should be displayed.
        """

        response = self.client.get(reverse('rango:index'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'There are no categories present.')
        self.assertQuerysetEqual(response.context['categories'], [])

    def test_index_views_with_categories(self):
        """
        Checks whether categories are displayed correctly when present
        """
        
        add_category('Python', 1, 1)
        add_category('C++', 1, 1)
        add_category('Erlang', 1, 1)

        response = self.client.get(reverse('rango:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Python")
        self.assertContains(response, "C++")
        self.assertContains(response, "Erlang")

        num_categories = len(response.context['categories'])
        self.assertEqual(num_categories, 3)

class GoToViewTests(TestCase):
    def setUp(self):
        # Set up some categories and pages for testing
        category = add_category('Python', 1, 1)
        self.page = Page.objects.create(
            title='Python Documentation',
            category=category,
            url='https://python.org',
            views=0,
            last_visit=timezone.now() - timedelta(days=1)  # Set last_visit to 1 day ago
        )

    def test_last_visit_not_in_future(self):
        """
        Ensure that the last visit is never set to a time in the future.
        """

        response = self.client.get(reverse('rango:goto') + f'?page_id={self.page.id}')
        self.page.refresh_from_db()

        self.assertTrue(self.page.last_visit <= timezone.now())

    def test_last_visit_updated_on_request(self):
        """
        Ensures that last_visit is updated when page is requested.
        """

        initial_last_visit = self.page.last_visit

        response = self.client.get(reverse('rango:goto') + f'?page_id={self.page.id}')
        self.page.refresh_from_db()

        self.assertNotEqual(initial_last_visit, self.page.last_visit)
        self.assertTrue(self.page.last_visit <= timezone.now())


def add_category(name, views=0, likes=0):
    category = Category.objects.get_or_create(name=name)[0]
    category.views = views
    category.likes = likes

    category.save()
    return category