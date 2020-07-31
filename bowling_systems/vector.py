from .bowling_system import BowlingSystem

class VectorThreeOne(BowlingSystem):

    tables = [
        '[CLASSIC_LANELOG].[dbo].[LANELOG]',
        '[CLASSIC_POS].[dbo].[RECEIPT_RECORD]',
        '[CLASSIC_POS].[dbo].[PLU_LIST]',
        '[CLASSIC_POS].[dbo].[RECEIPT]',
        '[CLASSIC_BOWLING].[dbo].[SCORE_DATA]',
        '[CLASSIC_BOWLING].[dbo].[WAITLIST]',
        '[CLASSIC_BOWLING].[dbo].[RESERVATION]',
        '[CLASSIC_BOWLING].[dbo].[ERROR_LOG]',
        '[CLASSIC_BOWLING].[dbo].[SETUP]'
    ]

    date_paths = {
        '[CLASSIC_LANELOG].[dbo].[LANELOG]':'start_time',
        '[CLASSIC_BOWLING].[dbo].[ERROR_LOG]':'log_date',
        '[CLASSIC_BOWLING].[dbo].[RESERVATION]': 'start_ time',
        '[CLASSIC_POS].[dbo].[RECEIPT]': 'date',
        '[CLASSIC_BOWLING].[dbo].[WAITLIST]': 'company_time'
    }

    """ Brunswick Vector 3 """
    def get_log_lanes(self):
        query = """
            SELECT l.lanelog_id, l.lane, l.ongoing, l.start_time, l.end_time,
            l.frames, l.employee, e.name
            FROM CLASSIC_LANELOG.dbo.LANELOG l
            LEFT JOIN CLASSIC_POS.dbo.EMPLOYEE e ON l.employee = e.id
            AND l.employee = e.id OR l.employee IS NULL
            WHERE l.start_time BETWEEN convert(datetime, '{start_time}')
			AND convert(datetime, '{end_time}')
            ORDER BY l.lanelog_id DESC
        """
        return self.get_from_sql_server(query.format(
            start_time=self.start_time,
            end_time=self.end_time
        ))
    
    def get_lane_errors_and_events(self):
        query = """
            SELECT log_id, log_date, lane, severity, data, source, long_description, short_description
            FROM CLASSIC_BOWLING.dbo.ERROR_LOG
            WHERE log_date BETWEEN convert(datetime, '{start_time}')
			AND convert(datetime, '{end_time}')
            ORDER BY log_id DESC
        """
        return self.get_from_sql_server(query.format(
            start_time=self.start_time,
            end_time=self.end_time
        ))

    def get_lanes_reservations(self):
        query = """
            SELECT reservation_id, lane, name, start_time, end_time, modification_time
            FROM CLASSIC_BOWLING.dbo.RESERVATION
            WHERE start_time BETWEEN convert(datetime, '{start_time}')
			AND convert(datetime, '{end_time}')
            ORDER BY reservation_id DESC
        """
        return self.get_from_sql_server(query.format(
            start_time=self.start_time,
            end_time=self.end_time
        ))

    def get_sales_details(self):
        query = """
            SELECT lt.receipt_id, lt.receipt_record_id, lt.plu_id, p.description, 
            lt.quantity, lt.rate_used, lt.total, lt.lanelog_id
            FROM CLASSIC_POS.dbo.RECEIPT_RECORD lt, CLASSIC_POS.dbo.PLU_LIST p
            WHERE (lt.plu_id = p.plu_id)
            ORDER BY lt.receipt_id DESC, lt.receipt_record_id ASC
        """
        return self.get_from_sql_server(query)

    def get_pos_tickets(self):
        query = """
            SELECT t.receipt_id, t.date, t.employee, e.name, t.total
            FROM CLASSIC_POS.dbo.RECEIPT t, CLASSIC_POS.dbo.EMPLOYEE e
			WHERE t.date BETWEEN convert(datetime, '{start_time}')
			AND convert(datetime, '{end_time}')
            AND (t.employee = e.id)
            ORDER BY receipt_id DESC
        """
        return self.get_from_sql_server(query.format(
            start_time=self.start_time,
            end_time=self.end_time
        ))

    def get_customers_waiting_list(self):
        query = """
            SELECT id, lanelog_id, company_name, company_time, num_players, player_1_name, player_2_name, player_3_name,
            player_4_name, player_5_name, player_6_name, player_7_name, player_8_name
            FROM CLASSIC_BOWLING.dbo.WAITLIST
            WHERE company_time BETWEEN convert(datetime, '{start_time}')
			AND convert(datetime, '{end_time}')
            ORDER BY id DESC
        """
        return self.get_from_sql_server(query.format(
            start_time=self.start_time,
            end_time=self.end_time
        ))

    def get_bowling_system_name(self):
        return 'BRUNSWICK_VECTOR3'



class VectorFive(BowlingSystem):
    """ Brunswick Vector 5 """
    def get_playing_lanes(self):
        pass
    
    def get_lane_errors_and_events(self):
        pass

    def get_lanes_reservations(self):
        pass

    def get_sales_details(self):
        pass

    def get_customers_waiting_list(self):
        pass

    def get_bowling_system_name(self):
        return 'BRUNSWICK_VECTOR5'