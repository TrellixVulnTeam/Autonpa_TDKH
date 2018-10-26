from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains as ac
from selenium.webdriver.common.keys import Keys as ks
from datetime import datetime as dt
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from time import sleep
import pytest
import csv
from openpyxl import load_workbook as lw
from openpyxl import Workbook
from openpyxl.compat import range
from openpyxl.utils import get_column_letter
from test_pyxl_lib import pyxl
import get_feature_bugs as gtb
import get_task_in_dev as gtid

@pytest.fixture
def driver(request):
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    wd = webdriver.Chrome(chrome_options=chrome_options)

    print(wd.capabilities)
    request.addfinalizer(wd.quit)
    return wd

# Фича-лист
# - добавить поле исправлено в версии (добавил)
# - Кастомизировать выгрузку под каждую вкладку отчета(кастомизировал только для вкладки в тестировании).
# - На очереди вкладка В разработке (кастомизировал).
# - На очереди остальные вкладки

filters_npa = [
["10765",  # задачи в разработке
 "10769", # задачи в тестировании
"10766", # задачи в аналитике
"10767", # закрытые задачи
"10770", # Открытые баги
"10772", # Закрытые баги
"10773"  # Отложенные задачи
],
 [
 'data\в_аналитике.csv',
 'data\закрытые_задачи.csv',
 'data\Открытые_баги.csv', 'data\закрытые_баги.csv', 'data\отложенные задачи.csv'
  ],
  ['В разработке',
   'В тестировании',
   'В аналитике',
  'Готовые задачи',
  'Открытые баги', 'Исправленные баги', 'Отложеные,отклоненные'
  ]
 ]

test_arr = ['NPA-1219', 'NPA-1429']

def test_main(driver):
    fn = str(gtb.login(driver))
    driver.get('http://jira.it2g.ru/issues/?jql=')
    sleep(0.5)
    tsk_list, iss = [],[]
    #counter = 0
    dest_file = 'data\\' + fn
    for t in range(len(filters_npa[0])):
        counter = 0
        #dest_file = 'data\\' + fn
        if filters_npa[2][t] == 'В разработке':
            # Найти все задачи по фильтру В разработке.
            iss_lst = gtb.get_tasks_list(driver, filters_npa[0][t], 'Release 5, ')

            # Находим данные по каждой задаче и записываем их в итоговую таблицу
            #count = 0
            for x in range(len(iss_lst)):
                iss = gtid.dev_tsk_data(driver, iss_lst[x])

                # Вызываем функцию записи в файл.
                counter = gtid.write_to_xls(iss, dest_file, filters_npa[2][t], counter)
        print(filters_npa[2][t])

        if filters_npa[2][t] == 'В тестировании':
            tsk_list = gtb.get_tasks_list(driver, "10769", 'Release 5, ')
            #print(tsk_list)
            for u in range(len(tsk_list)):
                # try:
                #     bgs = gtb.search_data(driver, tsk_list[u])
                # except:
                #     print('Связанных багов нет.')
                #     bgs = []
                iss = gtid.dev_tsk_data(driver, tsk_list[u])
                counter = gtid.write_to_xls(iss, dest_file, filters_npa[2][t], counter)
            #gtb.write_quantity_of_task(dest_file, counter)
        #В аналитике
        if filters_npa[2][t] == 'В аналитике':
            tsk_list = gtb.get_tasks_list(driver, "10766", 'Release 5, ')
            #print(tsk_list)
            for u in range(len(tsk_list)):

                iss = gtid.dev_tsk_data(driver, tsk_list[u])

                counter = gtid.write_to_xls(iss, dest_file, filters_npa[2][t], counter)

    # Архивный код
    # generate_report(driver, 2)
    # pyxl(filters_npa[1][0], filters_npa[2][2], fn)
    # sleep(1)

    # #Закрытые задачи
    #     if filters_npa[2][t] == 'Готовые задачи':
    #         tsk_list = gtb.get_tasks_list(driver, "10767", 'Release 5, ')
    #         #print(tsk_list)
    #         for u in range(len(tsk_list)):
    #
    #             iss = gtid.dev_tsk_data(driver, tsk_list[u])
    #
    #             counter = gtid.write_to_xls(iss, dest_file, filters_npa[2][t], counter)
    #
    # # Архивный код
    # # generate_report(driver, 3)
    # # pyxl(filters_npa[1][1], filters_npa[2][3], fn)
    # # sleep(1)
    #
    # #Открытые баги
    #     if filters_npa[2][t] == 'Открытые баги':
    #         tsk_list = gtb.get_tasks_list(driver, "10770", 'Release 5, ')
    #         #print(tsk_list)
    #         for u in range(len(tsk_list)):
    #
    #             iss = gtid.dev_tsk_data(driver, tsk_list[u])
    #
    #             counter = gtid.write_to_xls(iss, dest_file, filters_npa[2][t], counter)
    #
    # # Архивный код
    # # generate_report(driver, 4)
    # # pyxl(filters_npa[1][2], filters_npa[2][4], fn)
    # # sleep(1)
    #
    # # Исправленные баги
    #     if filters_npa[2][t] == 'Исправленные баги':
    #         tsk_list = gtb.get_tasks_list(driver, "10772", 'Release 5, ')
    #         #print(tsk_list)
    #         for u in range(len(tsk_list)):
    #
    #             iss = gtid.dev_tsk_data(driver, tsk_list[u])
    #
    #             counter = gtid.write_to_xls(iss, dest_file, filters_npa[2][t], counter)
    # # Архивный код
    # # generate_report(driver, 5)
    # # pyxl(filters_npa[1][3], filters_npa[2][5], fn)
    # # sleep(1)
    #
    # # Отложенные задачи
    #     if filters_npa[2][t] == 'Отложеные,отклоненные':
    #         tsk_list = gtb.get_tasks_list(driver, "10773", 'Release 5, ')
    #         #print(tsk_list)
    #         for u in range(len(tsk_list)):
    #
    #             iss = gtid.dev_tsk_data(driver, tsk_list[u])
    #
    #             counter = gtid.write_to_xls(iss, dest_file, filters_npa[2][t], counter)
    # Архивный код
    # generate_report(driver, 6)
    # pyxl(filters_npa[1][4], filters_npa[2][6], fn)


# Архивный код
# def generate_report(driver, t):
#     driver.get(f'http://jira.it2g.ru/issues/?filter={filters_npa[0][t]}')
#     sleep(4)
#     curr_page_count, all_tasks = 0, 0
#     table_data = []
#     write_data(table_data, filters_npa[1][t-2], 'headers')
#     try:
#         all_tasks = driver.find_element_by_class_name('results-count-total').text
#         curr_page_count = driver.find_element_by_class_name('results-count-end').text
#         if int(curr_page_count) < int(all_tasks):
#             while int(curr_page_count) < int(all_tasks):
#                 table_data = get_data(driver)
#                 # Записываем в файл добытые данные...
#                 write_data(table_data, filters_npa[1][t-2], 'data')
#                 #print(table_data[0])
#                 driver.execute_script('$(".icon-next").click()')
#                 sleep(2)
#                 all_tasks = driver.find_element_by_class_name('results-count-total').text
#                 curr_page_count = driver.find_element_by_class_name('results-count-end').text
#         if int(curr_page_count) == int(all_tasks):
#             table_data = get_data(driver)
#             # Записываем в файл добытые данные...
#             write_data(table_data, filters_npa[1][t-2], 'data', True)
#
#     except:
#         print('нет счетчика задач, задач тоже нет')
#
#     # Проверяем содержимое файла...
#     #read_data(filters_npa[1][t], table_data)
#
# def get_data(driver):
#     types_of_tasks = []
#     task_id=[]
#     summary=[]
#     assignee=[]
#     assigned = []
#     statuses, priority = [], []
#     qa_assigned = []
#     qa = []
#     result = []
#     print('Функция запустилась!')
#     try:
#         types_of_tasks = driver.find_elements_by_class_name('issuetype')
#         types_of_tasks = [x.find_element_by_tag_name('img').get_attribute('alt') for x in types_of_tasks]
#
#         task_id = driver.find_elements_by_class_name('issuekey')
#         task_id = [x.find_element_by_tag_name('a').text for x in task_id]
#
#         summary = driver.find_elements_by_class_name('summary')
#         summary = [x.find_element_by_tag_name('p').text for x in summary]
#
#         statuses = driver.find_elements_by_class_name('status')
#         statuses = [x.find_element_by_tag_name('span').text for x in statuses]
#
#         priority = driver.find_elements_by_class_name('priority')
#         priority = [x.find_element_by_tag_name('img').get_attribute('alt') for x in priority]
#
#         assignee = driver.find_elements_by_class_name('assignee')
#         qa_assigned = driver.find_elements_by_css_selector('.customfield_10201')
#         sprint = driver.find_elements_by_class_name('fixVersions')
#         sprint = [x.text for x in sprint]
#         print(len(sprint))
#
#         for u in range(len(assignee)):
#             try:
#                 assigned.append(assignee[u].find_element_by_css_selector(' span a').text)
#             except:
#                 assigned.append(assignee[u].find_element_by_tag_name('em').text)
#             try:
#                 qa.append(qa_assigned[u].find_element_by_css_selector('span a').text)
#             except:
#                 qa.append('Не назначен')
#
#             assignee[u] = assigned[u]
#             qa_assigned[u] = qa[u]
#         temp_str = ''
#
#         for r in range(len(types_of_tasks)):
#             temp_str = f'{task_id[r]}|{types_of_tasks[r]}|{statuses[r]}|{priority[r]}|{summary[r]}|{assignee[r]}|{qa_assigned[r]}|{sprint[r]}'.split(';')
#             result.append(temp_str)
#         print(result[0])
#         return result
#     except:
#         print('Задач нет')
#         return ''
# # Переписать функцию, чтобы писала сразу в excel для каждой вкладки свои данные
# def write_data(data, path, trigger='headers', end = False):
#     # в случае trigger = 'headers' в файл записывается строчка с заголовками столбцов
#     # в случае trigger = 'data' в файл записываются данные с задачами
#     with open(path, "a", newline='') as csv_file:
#         writer = csv.writer(csv_file, delimiter=';')
#
#         if trigger=='headers':
#             writer.writerow('№ в Jira|Тип задачи|Статус|Приоритет|Тема|Исполнитель|Тестировщик|Sprint'.split(';'))
#
#         if trigger == 'data':
#             for line in data:
#                 writer.writerow(line)
#         if end:
#             csv_file.close()
