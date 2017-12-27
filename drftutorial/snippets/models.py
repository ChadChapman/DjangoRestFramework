from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
"""
basic imports above, auth and permisisons imports below
"""
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight


LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item [0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())

class Snippet(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	title = models.CharField(max_length=100, blank=True, default='')
	code = models.TextField()
	linenos = models.BooleanField(default=False)
	language = models.CharField(choices=LANGUAGE_CHOICES, default='python3', max_length=100)
	style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)
	"""
	basic model attributes above, auth and permssions attrs. below
	"""
	owner = models.ForeignKey('auth.User', related_name='snippets', on_delete=models.CASCADE)
	highlighted = models.TextField()
	
	"""
	now add a save method to model (tut pt. 4)
	"""
	def save(self, *args, **kwargs):
		"""
		using pygments lib to create a highlighted html rep. of the snippet
		"""
		lexer = get_lexer_by_name(self.language)
		linenos = self.linenos and 'table' or False
		options = self.title and {'title': self.title} or ()
		formatter = HtmlFormatter(style=self.style, linenos=linenos, full=True, **options)
		self.highlighted = highlight(self.code, lexer, formatter)
		super(Snippet, self).save(*args, **kwargs)




	class Meta:
		ordering = ('created',)

