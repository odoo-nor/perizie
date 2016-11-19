# ----------------------
# Database Utilities
class DBUtils(object):
    # def __init__(self, db):
    # self.db = db

    '''
    Utility Methods
    '''

    def get_max_value(self, db):
        sql_query = '''
            SELECT MAX(forensics_reperto.numero_reperto)
            FROM forensics_reperto;
        '''
        db.execute(sql_query, )
        res = map(lambda x: x[0], db.fetchall())
        return res[0]
