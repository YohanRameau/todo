from datetime import datetime
from django.db import models
from django.utils import timezone

class Section(models.Model):
    """This is a conceptual class representation of a Section. 
    a section has composed by zero, one or many Tasks.
    The section name is unique, two sections can't have the same name.
    :param name
    :type  name: str
    :param pub_date
    :type  pub_date: datetime
    """
    name = models.CharField(max_length=200,unique=True)
    pub_date = models.DateTimeField(default=timezone.now)
    ordering=['pub_date']
    
    def __str__(self):
        return self.name
    
    def more_recent_task_date(self) ->datetime:
        """give the most recent task date or the published 
        section date if it have no task.

        :return: 
        :rtype: datetime
        """
        t = self.tasks
        if t.count() == 0:
            return self.pub_date
        return t.order_by('-pub_date').first().pub_date
    
    @property
    def tasks(self) -> models.query.QuerySet:
        """ This method provide all tasks from a section

        :return: QuerySet containing all tasks of the Section instance . 
        :rtype: models.query.QuerySet
        """
        return self.task_set.all()         


class Task(models.Model):
    """ This is a conceptual class representation of a Task
    :param  name : name of a Task
    :type   name : str
    :param  pub_date : Task publication date
    :type   pub_date : models.DateTimeField
    :param  deadline : Task deadline date, can be optional
    :type   deadline : models.DateTimeField, optional
    :param  section  : The section of this Task.
    :type   section  : class: Task.Section
    """
    name    = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date created', default=timezone.now)
    deadline = models.DateTimeField('dealine', null=True, blank=True)
    section  = models.ForeignKey(Section, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name + " " + self.section.__str__() + " " + self.pub_date.strftime("%d/%m/%Y")
    
    def is_late(self) -> bool:
        """[summary]

        :return: [description]
        :rtype: bool
        """
        
        return timezone.now() <= self.deadline if self.deadline is not None else False 