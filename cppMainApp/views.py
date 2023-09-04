import pandas
import io

from django.shortcuts import render
from rest_framework.views import APIView

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .utils import generate_table_html, ListOfDotDicts



class GetAllTablesNames(APIView):

    def get(self, request):
        cursor = request.db_connection.cursor()

        query = """
                SELECT json_agg(row_to_json(row)) AS result FROM (
                                    SELECT * from poc.model_details
                                ) row;
                """
        cursor.execute(query)
        model_details_result = cursor.fetchone()[0]


        query = """SELECT json_agg(row_to_json(row)) AS result
                FROM (
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'poc'
                ) row;"""
        cursor.execute(query)
        result_data = cursor.fetchone()[0]
        column_names = result_data[0].keys()
        print(column_names)
        print("#####")
        print(result_data)
        dot_data = ListOfDotDicts(result_data)
        
        table_thead_html, table_tbody_html = generate_table_html(result_data, 'all_table', None)

        # return render(request, 'table.html', {"columns": column_names, "data": result_data, "model_details": model_details_result, 'thead_html': table_thead_html, 'tbody_html': table_tbody_html})
        return render(request, 'table.html', {"columns": column_names, "data": dot_data, "model_details": model_details_result})


class GetAllDataSpecificTable(APIView):

    def get(self, request, table_name):
        model_id = request.GET.get('model_id')

        cursor = request.db_connection.cursor()


        query = f"""SELECT json_agg(row_to_json(row)) AS result
                FROM (
                    SELECT * from poc.{table_name} where model_id={model_id}
                ) row;"""
        
        cursor.execute(query)
        data = cursor.fetchone()[0]
        toGetColumns=data[0]
        column_names = list(toGetColumns.keys())
        # for key in toGetColumns.keys:
        #     column_names=column_names.append(key)
        print(column_names,777777777777777777777777777777777)
        # table_thead_html, table_tbody_html = generate_table_html(data, 'table_detail', table_name)
        # print(table_name,"Table Name")
        # print("table_thead_html",table_thead_html)

        # return render(request, 'table_detail.html', {"data": data, 'table_name': table_name, 'thead_html': table_thead_html, 'tbody_html': table_tbody_html})
        return render(request, 'table_detail.html',{"data":data,"colmn_names":column_names,"table_name":table_name})


@method_decorator(csrf_exempt, name='dispatch')
class UpdateDataSpecificTableViaUniqueIdentification(APIView):
    def post(self, request):
        update_values = request.data.get('data', '("7", "case 1", "Description 1", "false", "2023-05-31T14:36:15.526+05:30", "null")')
        condition = request.data.get('condition', 'id = 1')
        

        connection = request.db_connection
        cursor = connection.cursor()
        # query = f"SELECT column_name FROM information_schema.columns WHERE table_name = '{request.GET.get('table_name', 'pdi_app_case')}';"
        # cursor.execute(query)

        
        set_values = update_values
        sql_query = f"UPDATE poc.{request.data.get('table_name', 'pdi_app_case')} SET {set_values} WHERE {condition};"
        cursor.execute(sql_query)

        connection.commit()
        print("Rows updated successfully!")
        return JsonResponse({"data": "Updated"}, safe=False)

class UpdateDataSpecificTableViaFile(APIView):
    def post(self, request):
        # connection = request.db_connection
        cursor = request.db_connection.cursor()

        query = f"SELECT column_name FROM information_schema.columns where table_name = '{request.GET.get('table_name', 'pdi_app_case')}';"
        cursor.execute(query)
        table_columns = [row[0] for row in cursor.fetchall()]

        excel_data = request.FILES.get('File')

        excel_data = excel_data.read()
        df = pandas.read_csv(io.BytesIO(excel_data))
        dataframe = df.to_json(orient='records')

        value_list = dataframe.values.tolist()
        for value in value_list:
            query

        # for index, row in dataframe.iterrows():
        #     values = {}
        #     for i in zip(list(index),list(row)):
        #         values[i[0]] = i[1]
        #     print(values)

@method_decorator(csrf_exempt, name='dispatch')
class delete_table(APIView):
    def post(self, request):
        table_name = request.POST.get("Table_name")
        connection = request.db_connection
        cursor = connection.cursor()
        cursor.execute(f'DELETE FROM "{table_name}";')
        # cursor.close()
        connection.commit()
        return GetAllTablesNames().get(request)
    
@method_decorator(csrf_exempt, name='dispatch')
class DeleteEntryOfSpecificTable(APIView):
    def post(self, request):
        data_string=request.POST.get("case_id")
        table_name=request.POST.get("case_table_name")
        connection = request.db_connection
        cursor = connection.cursor()
        cursor.execute(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}';")
        column_names = [colmn[0] for colmn in cursor.fetchall()]
        Pk_index=column_names.index('personid')
        data_list=data_string.split(',')
        cursor.execute(f"DELETE FROM {table_name} WHERE personid = {data_list[Pk_index]}")
        connection.commit()
        return GetAllDataSpecificTable().get(request,table_name)
    
@method_decorator(csrf_exempt, name='dispatch')
class update_entry(APIView):
    def post(self, request):
        table_name=request.POST.get("table_name")
        connection = request.db_connection
        cursor = connection.cursor()
        query = f"SELECT column_name FROM information_schema.columns where table_name = '{table_name}';"
        cursor.execute(query)
        table_columns = [row[0] for row in cursor.fetchall()]
        print(table_columns)
        # column_names = [colmn[0] for colmn in cursor.fetchall()]
        # index=column_names.index('personid')
        # insertion_data=''
        # for column in column_names:
        #     temp = request.POST.get(f"set{column}")
        #     if column == "personid":
        #         pass
        #     elif insertion_data:
        #         insertion_data = insertion_data + ',' + column + '=' + "'" + temp + "'"
        #     else:
        #         insertion_data = column + '=' +  "'" + temp + "'"
        # cursor.execute(f"UPDATE {table_name} SET {insertion_data} WHERE personid = {old_data_list[index]};")

        # connection.commit()
        return GetAllDataSpecificTable().get(request,table_name)
            
            



