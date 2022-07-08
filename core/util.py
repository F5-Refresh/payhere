class DeleteFlag:

    '''카테고리 View

    Writer: 이동연
    Date: 2022-07-05

    delete_flag에 대한 처리를 담당합니다.
    '''

    def toggle_active(self):
        self.delete_flag = not self.delete_flag
        self.save()
        message = '삭제' if self.delete_flag else '복구'
        self.delete_message = {'success': f'정상적으로 {message}가 되었습니다.'}

    class Meta:
        abstract = True
