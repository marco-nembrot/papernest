
import json
from typing import Union
from fastapi import FastAPI, HTTPException

import dataframe
import functions


api = FastAPI()

@api.get("/")
def read_root(q: Union[str, None] = None):

    try:
        DF = dataframe.Dataframe().get()
    except FileNotFoundError:
        raise HTTPException(status_code=400, detail="Main file's not processed. Please, process file first.")
    else:
        if q is None or len(q) <= 2:
            raise HTTPException(status_code=400, detail="No given address. Address should have at least three characters.")
        else:
            postcode = functions.get_postcode(functions.get_query_data(q))
            #postcode = '29242'
            city_df = DF[DF['postcode'] == postcode]

            if len(city_df.index) == 0:
                raise HTTPException(status_code=404, detail="No coverage information for the given address.")
            else :
                # Using built-in pandas function to get as close to outpput format as possible
                # -- removing postcode column
                # -- converting coverage values to boolean (to int first since they're string)
                city_df = city_df.drop(columns=['postcode'])
                city_df.iloc[:, 1:] = city_df.iloc[:, 1:].astype(int)
                city_df.iloc[:, 1:] = city_df.iloc[:, 1:].astype(bool)

                data = json.loads(city_df.to_json(orient='table', index=False))['data']
                output = {}
                for result in data:
                    operator = result['Operateur']
                    del result['Operateur']
                    output[operator] = result
            
                return output
