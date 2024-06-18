from django.contrib import auth
from django.db import models


class Publisher(models.Model):
    """Компания, которая издает книги."""
    name = models.CharField(max_length=50, help_text="Название издательства")
    website = models.URLField(help_text="Веб-сайт издателя")
    email = models.EmailField(help_text="Адрес электронной почты Издателя")

    def __str__(self):
        return self.name

class Book(models.Model):
    """Опубликованная книга"""
    title = models.CharField(max_length=70, help_text="Название книги")
    publication_date = models.DateField(verbose_name="Дата издательства")
    isbn = models.CharField(max_length=20, verbose_name="ISBN-номер книги")
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    contributors = models.ManyToManyField('Contributor', through='BookContributor')

    def isbn13(self):
        """ '9780316769174' => '978-0-31-676917-4' """
        return "{}-{}-{}-{}-{}".format(self.isbn[0:3], self.isbn[3:4], self.isbn[4:6], self.isbn[6:12], self.isbn[12:13])

    def __str__(self):
        return "{} ({})".format(self.title, self.isbn)

class Contributor(models.Model):
    """ Участник, внесший вклад в книгу, например, автор, редактор, соавтор."""
    first_names = models.CharField(max_length=50, help_text="Имя/имена участника/ов.")
    last_names = models.CharField(max_length=50, help_text="Фамилия/фамилии участника/ов")
    email = models.EmailField(help_text="Контактный адрес электронной почты участника")

    def initialled_name(self):
        """ self.first_names='Jerome David', self.last_names='Salinger'
            => 'Salinger, JD' """
        initials = ''.join([name[0] for name
                            in self.first_names.split(' ')])
        return "{}, {}".format(self.last_names, initials)

    def __str__(self):
        return self.initialled_name()

class BookContributor(models.Model):
    class ContributionRole(models.TextChoices):
        AUTHOR = "AUTHOR", "Author"
        CO_AUTHOR = "CO_AUTHOR", "Co-Author"
        EDITOR = "EDITOR", "Editor"

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    contributor = models.ForeignKey(Contributor, on_delete=models.PROTECT)
    role = models.CharField(verbose_name="Роль, которую сыграл этот автор в создании книги",
                            choices=ContributionRole.choices, max_length=20)

    def __str__(self):
        return "{} {} {}".format(self.contributor.initialled_name(), self.role, self.book.isbn)

class Review(models.Model):
    content = models.TextField(help_text="Текст рецензии")
    rating = models.IntegerField(help_text="Оценка, данная рецензентом")
    date_created = models.DateTimeField(auto_now_add=True, help_text="Дата и время создания обзора")
    date_edited = models.DateTimeField(null=True, help_text="Дата и время последнего изменения обзора")
    creator = models.ForeignKey(auth.get_user_model(), on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, help_text="Книга, для которой предназначен этот обзор")

    def __str__(self):
        return "{} - {}".format(self.creator.username, self.book.title)