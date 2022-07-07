class DeleteFlag:

    def toggle_active(self):
        self.delete_flag = not self.delete_flag
        self.save()
    
    class Meta:
        abstract = True