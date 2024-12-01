import sys
sys.path.insert(0, '../src')

import os
from dataclasses import dataclass
import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from src.utils import save_object
from src.exception import CustomException
from src.logger import logging



@dataclass  # to avoid the construct we use the decorator here
class DataTransformationConfig:
    preproccessor_object_path = os.path.join('artifacts','preprocessor.pkl')



class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_transformer(self):
        """
        Function responsible for data transformation
        """
        try:
            cat_feature =['gender', 'race_ethnicity', 'parental_level_of_education', 'lunch',
            'test_preparation_course']
            num_featured = ['math_score', 'reading_score','writing_score', 'average_score']

            num_pipeline = Pipeline(
              steps = [
                  ("imputer", SimpleImputer(strategy='median')),
                ('scaler', StandardScaler())
              ]
          )
            
            cat_pipeline =Pipeline(
                steps=[
                    ('imputer', SimpleImputer(strategy='mode')),
                    ('one_hot_encoder', OneHotEncoder()),
                    ('scaler', StandardScaler())
                ]
            )
            logging.info("Numerical standard scaling completed")
            logging.info("Categorical column encoding completed")


            
            preprocessor = ColumnTransformer(
                [
                    ('num_pipeline', num_pipeline, num_featured),
                    ('cat_pipeline', cat_pipeline, cat_feature)
                ]
            )

            return preprocessor
        
        except Exception as e:
            raise CustomException(e, sys)
        
    
    def initiate_data_transformation(self, train_path, test_path):
        try:
            train_df =pd.read_csv(train_path)
            test_df =pd.read_csv(test_path)
            
            logging.info('Read the data')
            logging.info('Obtaining preprocessing object')

            preprocess_object = self.get_transformer()

            target_col = 'total_score'
            num_featured = ['math_score', 'reading_score','writing_score', 'average_score']

            input_feature_train = train_df.drop(columns = [target_col],axis=1)
            target_train_col = train_df[target_col]
            
            input_feature_test = test_df.drop(columns = [target_col],axis=1)
            target_test_col = test_df[target_col]

            logging.info("Applying preprocessing object on training df")

            input_feature_train_arr = preprocess_object.fit_transform(input_feature_train)
            
            input_feature_test_arr =  preprocess_object.transform(input_feature_test)

            train_arr =np.c_[
                input_feature_train_arr, np.array(target_train_col)
            ]

            test_arr = np.c_[
                input_feature_test_arr, np.array(target_test_col)
            ]

            logging.info("Saved preprocessing object")
            save_object(
                file_path=self.data_transformation_config.preproccessor_object_path,
                obj = preprocess_object
            )
            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preproccessor_object_path
            )
        except Exception as e:
            raise CustomException(e,sys)
            

            
        
