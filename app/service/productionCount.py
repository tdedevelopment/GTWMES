import os
import sys
import time

from service.message import MessageService
from dao.activeTime import ActiveTimeDAO 
from dao.configuration import ConfigurationDAO
from dao.productionCount import ProductionCountDAO


sys.path.append(os.path.join(os.path.dirname(__file__), '../database'))
import connectDB
from config import load_config

def productionCount(client, topicSend):
    config = load_config()
    conn = connectDB.connect(config)
    start = time.time()            
    

    configuration_dao = ConfigurationDAO(conn)
    active_time_dao = ActiveTimeDAO(conn)
    production_count_dao = ProductionCountDAO(conn)

    final_pos = production_count_dao.getPOs()

    while True:
        end = time.time()
        length = end - start
        for po in final_pos:
            if(round(round(length) % po['p_timer_communication_cycle']) == 0 and round(length) != 0):
                already_exist_this_equipmentId_at_active_time = active_time_dao.getActiveTimeByEquipmentId(po['equipment_id'])
        
                if already_exist_this_equipmentId_at_active_time != None:
                    #if exists, set equipment active time
                    active_time_dao.setActiveTime(po['equipment_id'], int(already_exist_this_equipmentId_at_active_time['active_time']) + po['p_timer_communication_cycle'])
                else:
                    #if not, create active time for this equipment 
                    active_time_dao.insertActiveTime(po['equipment_id'], round(length))
                
                message_service = MessageService(configuration_dao, active_time_dao)
                message_service.sendProductionCount(client, topicSend, po)

        final_pos = production_count_dao.getPOs()
        
        time.sleep(1)