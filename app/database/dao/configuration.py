import logging
import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor

class ConfigurationDAO:
    def __init__(self, connection):
        self.connection = connection

    def getCountingEquipmentByCode(self, data):
        try:
            with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
                check_if_counting_equipment_exists_query = sql.SQL("""
                SELECT *
                FROM counting_equipment
                WHERE code = %s
                LIMIT 1
                """)
                cursor.execute(check_if_counting_equipment_exists_query, (data["equipmentCode"],))
                equipment_found = cursor.fetchone()
                return equipment_found
            
        except Exception as err:
            logging.error("%s. getCountingEquipmentByCode failed", err)

    def getCountingEquipmentAll(self):
        try:
            with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
                get_all_counting_equipment_query = sql.SQL("""
                SELECT *
                FROM counting_equipment
                """)
                cursor.execute(get_all_counting_equipment_query)
                equipment_found = cursor.fetchall()
                return equipment_found
            
        except Exception as err:
            logging.error("%s. getCountingEquipmentAll failed", err)

    def insertCountingEquipment(self, data):
        try:
            with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
                new_counting_equipment_query = """
                INSERT INTO counting_equipment (code, equipment_status, p_timer_communication_cycle)
                VALUES (%s, %s, %s)
                RETURNING code;
                """
                cursor.execute(new_counting_equipment_query, (data["equipmentCode"], 0, data["pTimerCommunicationCycle"]))
                inserted_counting_equipment_id = cursor.fetchone()
                self.connection.commit()
                print("Insert counting_equipment: " + data["equipmentCode"])
                return inserted_counting_equipment_id['code']
            
        except Exception as err:
            logging.error("%s. insertCountingEquipment failed", err)

    def updateCountingEquipment(self, data):
        try:
            with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
                update_counting_equipment_query = sql.SQL("""
                UPDATE counting_equipment
                SET equipment_status = %s,
                p_timer_communication_cycle = %s
                WHERE code = %s
                RETURNING code
                """)
                cursor.execute(update_counting_equipment_query, (0, data["pTimerCommunicationCycle"], data["equipmentCode"]))
                
                updated_counting_equipment_id = cursor.fetchone()
                self.connection.commit()
                print("Updated counting_equipment: " + data["equipmentCode"])
                return updated_counting_equipment_id['code']
        
        except Exception as err:
            logging.error("%s. updateCountingEquipment failed", err)

    def getEquipmentOutputByEquipmentId(self, data):
        try:
            with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
                get_equipment_output_query = sql.SQL("""
                SELECT *
                FROM equipment_output
                WHERE equipment_code = %s AND disable = %s
                """)
                cursor.execute(get_equipment_output_query, (data, 0))
                equipment_output_found = cursor.fetchall()
                return equipment_output_found
            
        except Exception as err:
            logging.error("%s. getEquipmentOutputByEquipmentId failed", err)

    def getEquipmentOutputByEquipmentIdAndCode(self, data, code):
        try:
            with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
                get_equipment_output_query = sql.SQL("""
                SELECT *
                FROM equipment_output
                WHERE equipment_code = %s AND disable = %s AND code = %s
                """)
                cursor.execute(get_equipment_output_query, (data, 0, code))
                equipment_output_found = cursor.fetchall()
                return equipment_output_found
            
        except Exception as err:
            logging.error("%s. getEquipmentOutputByEquipmentIdAndCode failed", err)
        
    def getEquipmentOutput(self):
        try:
            with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
                get_equipment_output_query = sql.SQL("""
                SELECT *
                FROM equipment_output
                """)
                cursor.execute(get_equipment_output_query)
                equipment_output_found = cursor.fetchall()
                return equipment_output_found
            
        except Exception as err:
            logging.error("%s. getEquipmentOutput failed", err)

    def insertEquipmentOutput(self, inserted_ce_code, data):
        try:
            with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
                new_equipment_output_query = """
                    INSERT INTO equipment_output (equipment_code, code)
                    VALUES (%s, %s);
                    """
                for output in data["outputCodes"]:
                    cursor.execute(new_equipment_output_query, (inserted_ce_code, output))
                    self.connection.commit()
                    print("Insert equipment_output: " + output)

        except Exception as err:
            logging.error("%s. insertEquipmentOutput failed", err)

    def deleteEquipmentOutput(self, updated_ce_code):
        try:
            with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
                delete_existing_outputs = sql.SQL("""
                DELETE
                FROM equipment_output
                WHERE equipment_code = %s
                """)
                cursor.execute(delete_existing_outputs, (updated_ce_code,))
                self.connection.commit()

        except Exception as err:
            logging.error("%s. deleteEquipmentOutput failed", err)

    def updateEquipmentOutputDisable(self, equipment_code, code, disable):
        try:
            with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
                update_disable_output_query = sql.SQL("""
                UPDATE equipment_output
                SET disable = %s
                WHERE code = %s AND equipment_code = %s
                """)
                cursor.execute(update_disable_output_query, (disable, code, equipment_code))
                self.connection.commit()
                print("Updated output")

        except Exception as err:
            logging.error("%s. updateEquipmentOutputDisable failed", err)
