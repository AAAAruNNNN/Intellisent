from django.db import models

class Channel(models.Model):
    channel_id = models.CharField(max_length=50)
    name = models.CharField(max_length=20, default=None)
    image = models.CharField(max_length=100, default=None)
    language = models.CharField(default='English', max_length=10)
    def __str__(self):
        return("{} ({})".format(self.name, self.language))

class Program(models.Model):
    channel = models.ForeignKey('Channel', on_delete=models.CASCADE)
    program_id = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    image = models.CharField(max_length=100, default=None)
    genre = models.CharField(max_length=20)
    duration = models.IntegerField(default=0)
    def __str__(self):
        return("{} ({}) - {} minutes".format(self.name, self.channel.name, self.duration))

class Episode(models.Model):
    program = models.ForeignKey('Program', on_delete=models.CASCADE)
    airdate = models.DateField()
    airtime = models.DateTimeField()
    endtime = models.DateTimeField()
    def __str__(self):
        return("{} - {} - ({} - {})".format(self.program.name, self.airdate, self.airtime, self.endtime))