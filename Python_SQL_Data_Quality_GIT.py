############################################  PROJECT DATA QUALITY ###############################################
############################################    PY/SQL  ###############################################
#################################### https://github.com/JapaDash #########################################
###### Author: JapaDash


{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Query builder SQL - Data Quality"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Author: JapaDash<br/>\n",
    "Last Update: 2020/02/14"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [],
   "source": [
    "import pyhdb\n",
    "import pandas as pd\n",
    "import matplotlib.pyplot as plt\n",
    "import numpy as np\n",
    "\n",
    "pd.set_option('display.max_columns', None)\n",
    "pd.set_option('display.max_rows', None)\n",
    "\n",
    "connect = pyhdb.connect(\n",
    "        host=\"by-dch2nh01.de.bayer.cnb\",\n",
    "        port=35015,\n",
    "        user=\"\",\n",
    "        password=\"\"\n",
    "    )\n",
    "\n",
    "cursor = connect.cursor()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [],
   "source": [
    "tabela = \"\"\" \"_SYS_BIC\".\"countries.bra.cs.sandbox.0001.enduser.household/CV_HOUSEHOLD_001\" \"\"\""
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {},
   "outputs": [],
   "source": [
    "query=\"\"\"\n",
    "SELECT * FROM \"\"\"+tabela+\"\"\"\n",
    "LIMIT 2\n",
    "\"\"\"\n",
    "\n",
    "cursor.execute(query)\n",
    "\n",
    "column_names = list(map(lambda x: x[0], cursor.description))\n",
    "\n",
    "#column_string = [r for r in column_names if r not in numeric_column]"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Missing values for string columns"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {},
   "outputs": [],
   "source": [
    "wierd_values=\"\"\" 'n/a','N/A','na','NA','nan','NAN','ns','NS','?','',' ','$','#N/A',\\\n",
    "'(VAZIO)','(BLANK)' ,'.', '0' \"\"\""
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {},
   "outputs": [],
   "source": [
    "S1='WITH tab1 AS ( \\nSELECT \\n'\n",
    "for i in range(0,len(column_names)-1):\n",
    "    S1+=column_names[i]+\",\\n\"\n",
    "S2=S1+\"CAST(\"+column_names[-1]+\" AS VARCHAR) AS \"+column_names[-1]+\",\\n\"\n",
    "\n",
    "S3=''\n",
    "for i in range(0,len(column_names)-1):\n",
    "    S3+=\"CASE WHEN \"\"\"+column_names[i]+\"\"\" IN (\"\"\"+wierd_values+\"\"\") \n",
    "    THEN NULL ELSE \"\"\"+column_names[i]+\"\"\" END TRANSF_\"\"\"+column_names[i]+\",\\n\"\n",
    "S4=S3+\"CASE WHEN CAST(\"\"\"+column_names[-1]+\"\"\" AS VARCHAR) IN (\"\"\"+wierd_values+\"\"\") \n",
    "    THEN NULL ELSE CAST(\"\"\"+column_names[-1]+\"\"\" AS VARCHAR) END TRANSF_\"\"\"+column_names[-1]\n",
    "S5=S2+S4+\"\"\"\\n FROM \"\"\"+tabela+\"\"\" )\"\"\" \n",
    "\n",
    "\n",
    "S6=S5+'\\n SELECT\\nSOURCE_SYSTEM,\\nCOUNT(*) AS TOTAL, \\n'\n",
    "for i in range(0,len(column_names)):\n",
    "    S6+=\"\"\"COUNT(*) - COUNT(\"\"\"+column_names[i]+\"\"\") AS RAW_COUNT_\"\"\"+column_names[i]+\"\"\", \\n\"\"\"\n",
    "\n",
    "S7=''\n",
    "for i in range(0,len(column_names)-1):\n",
    "    S7+=\"\"\"COUNT(*) - COUNT(TRANSF_\"\"\"+column_names[i]+\"\"\") AS TRANSF_COUNT_\"\"\"+column_names[i]+\"\"\", \\n\"\"\" \n",
    "S8=S7+\"\"\"COUNT(*) - COUNT(TRANSF_\"\"\"+column_names[-1]+\"\"\") AS TRANSF_COUNT_\"\"\"+column_names[-1]+\"\"\"\n",
    "FROM tab1\\nGROUP BY SOURCE_SYSTEM\"\"\"\n",
    "\n",
    "missing_query = S6+S8"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "WITH tab1 AS ( \n",
      "SELECT \n",
      "OPERATION,\n",
      "SOURCE_SYSTEM,\n",
      "SALES_REGION,\n",
      "CROP_YEAR,\n",
      "COUNTRY,\n",
      "PARTNER_ROOT_ID,\n",
      "PARTNER_NR_CNPJ,\n",
      "ACCNT_STATE,\n",
      "ACCNT_CITY_NAME,\n",
      "ACCNT_CITY_CODE,\n",
      "ACCNT_NAME,\n",
      "ACCNT_ROOT_ID,\n",
      "ACCNT_CD_DOCUMENT,\n",
      "ACCNT_TYPE,\n",
      "ACCNT_SUBTYPE,\n",
      "ACCNT_SUBTYPE_ORI,\n",
      "ACCNT_TELEPHONE1,\n",
      "ACCNT_TELEPHONE2,\n",
      "ACCNT_EMAIL,\n",
      "NM_BUSINESS_GROUP,\n",
      "NM_BUSINESS_UNIT,\n",
      "PRODUCT_BRAND,\n",
      "ACCNT_GROUP_CD_DOCUMENT,\n",
      "ACCNT_GROUP_NAME,\n",
      "PARTNER_GROUP_CD_DOCUMENT,\n",
      "PARTNER_GROUP_NAME,\n",
      "LOYALTY_MON_1_1,\n",
      "LOYALTY_ELEITOS,\n",
      "LOYALTY_GDI,\n",
      "LOYALTY_KAM,\n",
      "LOYALTY_IMPULSO,\n",
      "LOYALTY_CLIMATE,\n",
      "TIERS_NUMBERS,\n",
      "FLAG_QION_LIMITATION,\n",
      "PARTNER_CP_CLASSIFICATION,\n",
      "PARTNER_CORN_CLASSIFICATION,\n",
      "WHOLESALER_CP_CLASSIFICATION,\n",
      "WHOLESALER_CORN_CLASSIFICATION,\n",
      "FLAG_INTEGRATION,\n",
      "CAST(AMOUNT AS VARCHAR) AS AMOUNT,\n",
      "CASE WHEN OPERATION IN ( 'n/a','N/A','na','NA','nan','NAN','ns','NS','?','',' ','$','#N/A','(VAZIO)','(BLANK)' ,'.', '0' ) \n",
      "    THEN NULL ELSE OPERATION END TRANSF_OPERATION,\n",
      "CASE WHEN SOURCE_SYSTEM IN ( 'n/a','N/A','na','NA','nan','NAN','ns','NS','?','',' ','$','#N/A','(VAZIO)','(BLANK)' ,'.', '0' ) \n",
      "    THEN NULL ELSE SOURCE_SYSTEM END TRANSF_SOURCE_SYSTEM,\n",
      "CASE WHEN SALES_REGION IN ( 'n/a','N/A','na','NA','nan','NAN','ns','NS','?','',' ','$','#N/A','(VAZIO)','(BLANK)' ,'.', '0' ) \n",
      "    THEN NULL ELSE SALES_REGION END TRANSF_SALES_REGION,\n",
      "CASE WHEN CROP_YEAR IN ( 'n/a','N/A','na','NA','nan','NAN','ns','NS','?','',' ','$','#N/A','(VAZIO)','(BLANK)' ,'.', '0' ) \n",
      "    THEN NULL ELSE CROP_YEAR END TRANSF_CROP_YEAR,\n",
      "CASE WHEN COUNTRY IN ( 'n/a','N/A','na','NA','nan','NAN','ns','NS','?','',' ','$','#N/A','(VAZIO)','(BLANK)' ,'.', '0' ) \n",
      "    THEN NULL ELSE COUNTRY END TRANSF_COUNTRY,\n",
      "CASE WHEN PARTNER_ROOT_ID IN ( 'n/a','N/A','na','NA','nan','NAN','ns','NS','?','',' ','$','#N/A','(VAZIO)','(BLANK)' ,'.', '0' ) \n",
      "    THEN NULL ELSE PARTNER_ROOT_ID END TRANSF_PARTNER_ROOT_ID,\n",
      "CASE WHEN PARTNER_NR_CNPJ IN ( 'n/a','N/A','na','NA','nan','NAN','ns','NS','?','',' ','$','#N/A','(VAZIO)','(BLANK)' ,'.', '0' ) \n",
      "    THEN NULL ELSE PARTNER_NR_CNPJ END TRANSF_PARTNER_NR_CNPJ,\n",
      "CASE WHEN ACCNT_STATE IN ( 'n/a','N/A','na','NA','nan','NAN','ns','NS','?','',' ','$','#N/A','(VAZIO)','(BLANK)' ,'.', '0' ) \n",
      "    THEN NULL ELSE ACCNT_STATE END TRANSF_ACCNT_STATE,\n",
      "CASE WHEN ACCNT_CITY_NAME IN ( 'n/a','N/A','na','NA','nan','NAN','ns','NS','?','',' ','$','#N/A','(VAZIO)','(BLANK)' ,'.', '0' ) \n",
      "    THEN NULL ELSE ACCNT_CITY_NAME END TRANSF_ACCNT_CITY_NAME,\n",
      "CASE WHEN ACCNT_CITY_CODE IN ( 'n/a','N/A','na','NA','nan','NAN','ns','NS','?','',' ','$','#N/A','(VAZIO)','(BLANK)' ,'.', '0' ) \n",
      "    THEN NULL ELSE ACCNT_CITY_CODE END TRANSF_ACCNT_CITY_CODE,\n",
      "CASE WHEN ACCNT_NAME IN ( 'n/a','N/A','na','NA','nan','NAN','ns','NS','?','',' ','$','#N/A','(VAZIO)','(BLANK)' ,'.', '0' ) \n",
      "    THEN NULL ELSE ACCNT_NAME END TRANSF_ACCNT_NAME,\n",
      "CASE WHEN ACCNT_ROOT_ID IN ( 'n/a','N/A','na','NA','nan','NAN','ns','NS','?','',' ','$','#N/A','(VAZIO)','(BLANK)' ,'.', '0' ) \n",
      "    THEN NULL ELSE ACCNT_ROOT_ID END TRANSF_ACCNT_ROOT_ID,\n",
      "CASE WHEN ACCNT_CD_DOCUMENT IN ( 'n/a','N/A','na','NA','nan','NAN','ns','NS','?','',' ','$','#N/A','(VAZIO)','(BLANK)' ,'.', '0' ) \n",
      "    THEN NULL ELSE ACCNT_CD_DOCUMENT END TRANSF_ACCNT_CD_DOCUMENT,\n",
      "CASE WHEN ACCNT_TYPE IN ( 'n/a','N/A','na','NA','nan','NAN','ns','NS','?','',' ','$','#N/A','(VAZIO)','(BLANK)' ,'.', '0' ) \n",
      "    THEN NULL ELSE ACCNT_TYPE END TRANSF_ACCNT_TYPE,\n",
      "CASE WHEN ACCNT_SUBTYPE IN ( 'n/a','N/A','na','NA','nan','NAN','ns','NS','?','',' ','$','#N/A','(VAZIO)','(BLANK)' ,'.', '0' ) \n",
      "    THEN NULL ELSE ACCNT_SUBTYPE END TRANSF_ACCNT_SUBTYPE,\n",
      "CASE WHEN ACCNT_SUBTYPE_ORI IN ( 'n/a','N/A','na','NA','nan','NAN','ns','NS','?','',' ','$','#N/A','(VAZIO)','(BLANK)' ,'.', '0' ) \n",
      "    THEN NULL ELSE ACCNT_SUBTYPE_ORI END TRANSF_ACCNT_SUBTYPE_ORI,\n",
      "CASE WHEN ACCNT_TELEPHONE1 IN ( 'n/a','N/A','na','NA','nan','NAN','ns','NS','?','',' ','$','#N/A','(VAZIO)','(BLANK)' ,'.', '0' ) \n",
      "    THEN NULL ELSE ACCNT_TELEPHONE1 END TRANSF_ACCNT_TELEPHONE1,\n",
      "CASE WHEN ACCNT_TELEPHONE2 IN ( 'n/a','N/A','na','NA','nan','NAN','ns','NS','?','',' ','$','#N/A','(VAZIO)','(BLANK)' ,'.', '0' ) \n",
      "    THEN NULL ELSE ACCNT_TELEPHONE2 END TRANSF_ACCNT_TELEPHONE2,\n",
      "CASE WHEN ACCNT_EMAIL IN ( 'n/a','N/A','na','NA','nan','NAN','ns','NS','?','',' ','$','#N/A','(VAZIO)','(BLANK)' ,'.', '0' ) \n",
      "    THEN NULL ELSE ACCNT_EMAIL END TRANSF_ACCNT_EMAIL,\n",
      "CASE WHEN NM_BUSINESS_GROUP IN ( 'n/a','N/A','na','NA','nan','NAN','ns','NS','?','',' ','$','#N/A','(VAZIO)','(BLANK)' ,'.', '0' ) \n",
      "    THEN NULL ELSE NM_BUSINESS_GROUP END TRANSF_NM_BUSINESS_GROUP,\n",
      "CASE WHEN NM_BUSINESS_UNIT IN ( 'n/a','N/A','na','NA','nan','NAN','ns','NS','?','',' ','$','#N/A','(VAZIO)','(BLANK)' ,'.', '0' ) \n",
      "    THEN NULL ELSE NM_BUSINESS_UNIT END TRANSF_NM_BUSINESS_UNIT,\n",
      "CASE WHEN PRODUCT_BRAND IN ( 'n/a','N/A','na','NA','nan','NAN','ns','NS','?','',' ','$','#N/A','(VAZIO)','(BLANK)' ,'.', '0' ) \n",
      "    THEN NULL ELSE PRODUCT_BRAND END TRANSF_PRODUCT_BRAND,\n",
      "CASE WHEN ACCNT_GROUP_CD_DOCUMENT IN ( 'n/a','N/A','na','NA','nan','NAN','ns','NS','?','',' ','$','#N/A','(VAZIO)','(BLANK)' ,'.', '0' ) \n",
      "    THEN NULL ELSE ACCNT_GROUP_CD_DOCUMENT END TRANSF_ACCNT_GROUP_CD_DOCUMENT,\n",
      "CASE WHEN ACCNT_GROUP_NAME IN ( 'n/a','N/A','na','NA','nan','NAN','ns','NS','?','',' ','$','#N/A','(VAZIO)','(BLANK)' ,'.', '0' ) \n",
      "    THEN NULL ELSE ACCNT_GROUP_NAME END TRANSF_ACCNT_GROUP_NAME,\n",
      "CASE WHEN PARTNER_GROUP_CD_DOCUMENT IN ( 'n/a','N/A','na','NA','nan','NAN','ns','NS','?','',' ','$','#N/A','(VAZIO)','(BLANK)' ,'.', '0' ) \n",
      "    THEN NULL ELSE PARTNER_GROUP_CD_DOCUMENT END TRANSF_PARTNER_GROUP_CD_DOCUMENT,\n",
      "CASE WHEN PARTNER_GROUP_NAME IN ( 'n/a','N/A','na','NA','nan','NAN','ns','NS','?','',' ','$','#N/A','(VAZIO)','(BLANK)' ,'.', '0' ) \n",
      "    THEN NULL ELSE PARTNER_GROUP_NAME END TRANSF_PARTNER_GROUP_NAME,\n",
      "CASE WHEN LOYALTY_MON_1_1 IN ( 'n/a','N/A','na','NA','nan','NAN','ns','NS','?','',' ','$','#N/A','(VAZIO)','(BLANK)' ,'.', '0' ) \n",
      "    THEN NULL ELSE LOYALTY_MON_1_1 END TRANSF_LOYALTY_MON_1_1,\n",
      "CASE WHEN LOYALTY_ELEITOS IN ( 'n/a','N/A','na','NA','nan','NAN','ns','NS','?','',' ','$','#N/A','(VAZIO)','(BLANK)' ,'.', '0' ) \n",
      "    THEN NULL ELSE LOYALTY_ELEITOS END TRANSF_LOYALTY_ELEITOS,\n",
      "CASE WHEN LOYALTY_GDI IN ( 'n/a','N/A','na','NA','nan','NAN','ns','NS','?','',' ','$','#N/A','(VAZIO)','(BLANK)' ,'.', '0' ) \n",
      "    THEN NULL ELSE LOYALTY_GDI END TRANSF_LOYALTY_GDI,\n",
      "CASE WHEN LOYALTY_KAM IN ( 'n/a','N/A','na','NA','nan','NAN','ns','NS','?','',' ','$','#N/A','(VAZIO)','(BLANK)' ,'.', '0' ) \n",
      "    THEN NULL ELSE LOYALTY_KAM END TRANSF_LOYALTY_KAM,\n",
      "CASE WHEN LOYALTY_IMPULSO IN ( 'n/a','N/A','na','NA','nan','NAN','ns','NS','?','',' ','$','#N/A','(VAZIO)','(BLANK)' ,'.', '0' ) \n",
      "    THEN NULL ELSE LOYALTY_IMPULSO END TRANSF_LOYALTY_IMPULSO,\n",
      "CASE WHEN LOYALTY_CLIMATE IN ( 'n/a','N/A','na','NA','nan','NAN','ns','NS','?','',' ','$','#N/A','(VAZIO)','(BLANK)' ,'.', '0' ) \n",
      "    THEN NULL ELSE LOYALTY_CLIMATE END TRANSF_LOYALTY_CLIMATE,\n",
      "CASE WHEN TIERS_NUMBERS IN ( 'n/a','N/A','na','NA','nan','NAN','ns','NS','?','',' ','$','#N/A','(VAZIO)','(BLANK)' ,'.', '0' ) \n",
      "    THEN NULL ELSE TIERS_NUMBERS END TRANSF_TIERS_NUMBERS,\n",
      "CASE WHEN FLAG_QION_LIMITATION IN ( 'n/a','N/A','na','NA','nan','NAN','ns','NS','?','',' ','$','#N/A','(VAZIO)','(BLANK)' ,'.', '0' ) \n",
      "    THEN NULL ELSE FLAG_QION_LIMITATION END TRANSF_FLAG_QION_LIMITATION,\n",
      "CASE WHEN PARTNER_CP_CLASSIFICATION IN ( 'n/a','N/A','na','NA','nan','NAN','ns','NS','?','',' ','$','#N/A','(VAZIO)','(BLANK)' ,'.', '0' ) \n",
      "    THEN NULL ELSE PARTNER_CP_CLASSIFICATION END TRANSF_PARTNER_CP_CLASSIFICATION,\n",
      "CASE WHEN PARTNER_CORN_CLASSIFICATION IN ( 'n/a','N/A','na','NA','nan','NAN','ns','NS','?','',' ','$','#N/A','(VAZIO)','(BLANK)' ,'.', '0' ) \n",
      "    THEN NULL ELSE PARTNER_CORN_CLASSIFICATION END TRANSF_PARTNER_CORN_CLASSIFICATION,\n",
      "CASE WHEN WHOLESALER_CP_CLASSIFICATION IN ( 'n/a','N/A','na','NA','nan','NAN','ns','NS','?','',' ','$','#N/A','(VAZIO)','(BLANK)' ,'.', '0' ) \n",
      "    THEN NULL ELSE WHOLESALER_CP_CLASSIFICATION END TRANSF_WHOLESALER_CP_CLASSIFICATION,\n",
      "CASE WHEN WHOLESALER_CORN_CLASSIFICATION IN ( 'n/a','N/A','na','NA','nan','NAN','ns','NS','?','',' ','$','#N/A','(VAZIO)','(BLANK)' ,'.', '0' ) \n",
      "    THEN NULL ELSE WHOLESALER_CORN_CLASSIFICATION END TRANSF_WHOLESALER_CORN_CLASSIFICATION,\n",
      "CASE WHEN FLAG_INTEGRATION IN ( 'n/a','N/A','na','NA','nan','NAN','ns','NS','?','',' ','$','#N/A','(VAZIO)','(BLANK)' ,'.', '0' ) \n",
      "    THEN NULL ELSE FLAG_INTEGRATION END TRANSF_FLAG_INTEGRATION,\n",
      "CASE WHEN CAST(AMOUNT AS VARCHAR) IN ( 'n/a','N/A','na','NA','nan','NAN','ns','NS','?','',' ','$','#N/A','(VAZIO)','(BLANK)' ,'.', '0' ) \n",
      "    THEN NULL ELSE CAST(AMOUNT AS VARCHAR) END TRANSF_AMOUNT\n",
      " FROM  \"_SYS_BIC\".\"countries.bra.cs.sandbox.0001.enduser.household/CV_HOUSEHOLD_001\"  )\n",
      " SELECT\n",
      "SOURCE_SYSTEM,\n",
      "COUNT(*) AS TOTAL, \n",
      "COUNT(*) - COUNT(OPERATION) AS RAW_COUNT_OPERATION, \n",
      "COUNT(*) - COUNT(SOURCE_SYSTEM) AS RAW_COUNT_SOURCE_SYSTEM, \n",
      "COUNT(*) - COUNT(SALES_REGION) AS RAW_COUNT_SALES_REGION, \n",
      "COUNT(*) - COUNT(CROP_YEAR) AS RAW_COUNT_CROP_YEAR, \n",
      "COUNT(*) - COUNT(COUNTRY) AS RAW_COUNT_COUNTRY, \n",
      "COUNT(*) - COUNT(PARTNER_ROOT_ID) AS RAW_COUNT_PARTNER_ROOT_ID, \n",
      "COUNT(*) - COUNT(PARTNER_NR_CNPJ) AS RAW_COUNT_PARTNER_NR_CNPJ, \n",
      "COUNT(*) - COUNT(ACCNT_STATE) AS RAW_COUNT_ACCNT_STATE, \n",
      "COUNT(*) - COUNT(ACCNT_CITY_NAME) AS RAW_COUNT_ACCNT_CITY_NAME, \n",
      "COUNT(*) - COUNT(ACCNT_CITY_CODE) AS RAW_COUNT_ACCNT_CITY_CODE, \n",
      "COUNT(*) - COUNT(ACCNT_NAME) AS RAW_COUNT_ACCNT_NAME, \n",
      "COUNT(*) - COUNT(ACCNT_ROOT_ID) AS RAW_COUNT_ACCNT_ROOT_ID, \n",
      "COUNT(*) - COUNT(ACCNT_CD_DOCUMENT) AS RAW_COUNT_ACCNT_CD_DOCUMENT, \n",
      "COUNT(*) - COUNT(ACCNT_TYPE) AS RAW_COUNT_ACCNT_TYPE, \n",
      "COUNT(*) - COUNT(ACCNT_SUBTYPE) AS RAW_COUNT_ACCNT_SUBTYPE, \n",
      "COUNT(*) - COUNT(ACCNT_SUBTYPE_ORI) AS RAW_COUNT_ACCNT_SUBTYPE_ORI, \n",
      "COUNT(*) - COUNT(ACCNT_TELEPHONE1) AS RAW_COUNT_ACCNT_TELEPHONE1, \n",
      "COUNT(*) - COUNT(ACCNT_TELEPHONE2) AS RAW_COUNT_ACCNT_TELEPHONE2, \n",
      "COUNT(*) - COUNT(ACCNT_EMAIL) AS RAW_COUNT_ACCNT_EMAIL, \n",
      "COUNT(*) - COUNT(NM_BUSINESS_GROUP) AS RAW_COUNT_NM_BUSINESS_GROUP, \n",
      "COUNT(*) - COUNT(NM_BUSINESS_UNIT) AS RAW_COUNT_NM_BUSINESS_UNIT, \n",
      "COUNT(*) - COUNT(PRODUCT_BRAND) AS RAW_COUNT_PRODUCT_BRAND, \n",
      "COUNT(*) - COUNT(ACCNT_GROUP_CD_DOCUMENT) AS RAW_COUNT_ACCNT_GROUP_CD_DOCUMENT, \n",
      "COUNT(*) - COUNT(ACCNT_GROUP_NAME) AS RAW_COUNT_ACCNT_GROUP_NAME, \n",
      "COUNT(*) - COUNT(PARTNER_GROUP_CD_DOCUMENT) AS RAW_COUNT_PARTNER_GROUP_CD_DOCUMENT, \n",
      "COUNT(*) - COUNT(PARTNER_GROUP_NAME) AS RAW_COUNT_PARTNER_GROUP_NAME, \n",
      "COUNT(*) - COUNT(LOYALTY_MON_1_1) AS RAW_COUNT_LOYALTY_MON_1_1, \n",
      "COUNT(*) - COUNT(LOYALTY_ELEITOS) AS RAW_COUNT_LOYALTY_ELEITOS, \n",
      "COUNT(*) - COUNT(LOYALTY_GDI) AS RAW_COUNT_LOYALTY_GDI, \n",
      "COUNT(*) - COUNT(LOYALTY_KAM) AS RAW_COUNT_LOYALTY_KAM, \n",
      "COUNT(*) - COUNT(LOYALTY_IMPULSO) AS RAW_COUNT_LOYALTY_IMPULSO, \n",
      "COUNT(*) - COUNT(LOYALTY_CLIMATE) AS RAW_COUNT_LOYALTY_CLIMATE, \n",
      "COUNT(*) - COUNT(TIERS_NUMBERS) AS RAW_COUNT_TIERS_NUMBERS, \n",
      "COUNT(*) - COUNT(FLAG_QION_LIMITATION) AS RAW_COUNT_FLAG_QION_LIMITATION, \n",
      "COUNT(*) - COUNT(PARTNER_CP_CLASSIFICATION) AS RAW_COUNT_PARTNER_CP_CLASSIFICATION, \n",
      "COUNT(*) - COUNT(PARTNER_CORN_CLASSIFICATION) AS RAW_COUNT_PARTNER_CORN_CLASSIFICATION, \n",
      "COUNT(*) - COUNT(WHOLESALER_CP_CLASSIFICATION) AS RAW_COUNT_WHOLESALER_CP_CLASSIFICATION, \n",
      "COUNT(*) - COUNT(WHOLESALER_CORN_CLASSIFICATION) AS RAW_COUNT_WHOLESALER_CORN_CLASSIFICATION, \n",
      "COUNT(*) - COUNT(FLAG_INTEGRATION) AS RAW_COUNT_FLAG_INTEGRATION, \n",
      "COUNT(*) - COUNT(AMOUNT) AS RAW_COUNT_AMOUNT, \n",
      "COUNT(*) - COUNT(TRANSF_OPERATION) AS TRANSF_COUNT_OPERATION, \n",
      "COUNT(*) - COUNT(TRANSF_SOURCE_SYSTEM) AS TRANSF_COUNT_SOURCE_SYSTEM, \n",
      "COUNT(*) - COUNT(TRANSF_SALES_REGION) AS TRANSF_COUNT_SALES_REGION, \n",
      "COUNT(*) - COUNT(TRANSF_CROP_YEAR) AS TRANSF_COUNT_CROP_YEAR, \n",
      "COUNT(*) - COUNT(TRANSF_COUNTRY) AS TRANSF_COUNT_COUNTRY, \n",
      "COUNT(*) - COUNT(TRANSF_PARTNER_ROOT_ID) AS TRANSF_COUNT_PARTNER_ROOT_ID, \n",
      "COUNT(*) - COUNT(TRANSF_PARTNER_NR_CNPJ) AS TRANSF_COUNT_PARTNER_NR_CNPJ, \n",
      "COUNT(*) - COUNT(TRANSF_ACCNT_STATE) AS TRANSF_COUNT_ACCNT_STATE, \n",
      "COUNT(*) - COUNT(TRANSF_ACCNT_CITY_NAME) AS TRANSF_COUNT_ACCNT_CITY_NAME, \n",
      "COUNT(*) - COUNT(TRANSF_ACCNT_CITY_CODE) AS TRANSF_COUNT_ACCNT_CITY_CODE, \n",
      "COUNT(*) - COUNT(TRANSF_ACCNT_NAME) AS TRANSF_COUNT_ACCNT_NAME, \n",
      "COUNT(*) - COUNT(TRANSF_ACCNT_ROOT_ID) AS TRANSF_COUNT_ACCNT_ROOT_ID, \n",
      "COUNT(*) - COUNT(TRANSF_ACCNT_CD_DOCUMENT) AS TRANSF_COUNT_ACCNT_CD_DOCUMENT, \n",
      "COUNT(*) - COUNT(TRANSF_ACCNT_TYPE) AS TRANSF_COUNT_ACCNT_TYPE, \n",
      "COUNT(*) - COUNT(TRANSF_ACCNT_SUBTYPE) AS TRANSF_COUNT_ACCNT_SUBTYPE, \n",
      "COUNT(*) - COUNT(TRANSF_ACCNT_SUBTYPE_ORI) AS TRANSF_COUNT_ACCNT_SUBTYPE_ORI, \n",
      "COUNT(*) - COUNT(TRANSF_ACCNT_TELEPHONE1) AS TRANSF_COUNT_ACCNT_TELEPHONE1, \n",
      "COUNT(*) - COUNT(TRANSF_ACCNT_TELEPHONE2) AS TRANSF_COUNT_ACCNT_TELEPHONE2, \n",
      "COUNT(*) - COUNT(TRANSF_ACCNT_EMAIL) AS TRANSF_COUNT_ACCNT_EMAIL, \n",
      "COUNT(*) - COUNT(TRANSF_NM_BUSINESS_GROUP) AS TRANSF_COUNT_NM_BUSINESS_GROUP, \n",
      "COUNT(*) - COUNT(TRANSF_NM_BUSINESS_UNIT) AS TRANSF_COUNT_NM_BUSINESS_UNIT, \n",
      "COUNT(*) - COUNT(TRANSF_PRODUCT_BRAND) AS TRANSF_COUNT_PRODUCT_BRAND, \n",
      "COUNT(*) - COUNT(TRANSF_ACCNT_GROUP_CD_DOCUMENT) AS TRANSF_COUNT_ACCNT_GROUP_CD_DOCUMENT, \n",
      "COUNT(*) - COUNT(TRANSF_ACCNT_GROUP_NAME) AS TRANSF_COUNT_ACCNT_GROUP_NAME, \n",
      "COUNT(*) - COUNT(TRANSF_PARTNER_GROUP_CD_DOCUMENT) AS TRANSF_COUNT_PARTNER_GROUP_CD_DOCUMENT, \n",
      "COUNT(*) - COUNT(TRANSF_PARTNER_GROUP_NAME) AS TRANSF_COUNT_PARTNER_GROUP_NAME, \n",
      "COUNT(*) - COUNT(TRANSF_LOYALTY_MON_1_1) AS TRANSF_COUNT_LOYALTY_MON_1_1, \n",
      "COUNT(*) - COUNT(TRANSF_LOYALTY_ELEITOS) AS TRANSF_COUNT_LOYALTY_ELEITOS, \n",
      "COUNT(*) - COUNT(TRANSF_LOYALTY_GDI) AS TRANSF_COUNT_LOYALTY_GDI, \n",
      "COUNT(*) - COUNT(TRANSF_LOYALTY_KAM) AS TRANSF_COUNT_LOYALTY_KAM, \n",
      "COUNT(*) - COUNT(TRANSF_LOYALTY_IMPULSO) AS TRANSF_COUNT_LOYALTY_IMPULSO, \n",
      "COUNT(*) - COUNT(TRANSF_LOYALTY_CLIMATE) AS TRANSF_COUNT_LOYALTY_CLIMATE, \n",
      "COUNT(*) - COUNT(TRANSF_TIERS_NUMBERS) AS TRANSF_COUNT_TIERS_NUMBERS, \n",
      "COUNT(*) - COUNT(TRANSF_FLAG_QION_LIMITATION) AS TRANSF_COUNT_FLAG_QION_LIMITATION, \n",
      "COUNT(*) - COUNT(TRANSF_PARTNER_CP_CLASSIFICATION) AS TRANSF_COUNT_PARTNER_CP_CLASSIFICATION, \n",
      "COUNT(*) - COUNT(TRANSF_PARTNER_CORN_CLASSIFICATION) AS TRANSF_COUNT_PARTNER_CORN_CLASSIFICATION, \n",
      "COUNT(*) - COUNT(TRANSF_WHOLESALER_CP_CLASSIFICATION) AS TRANSF_COUNT_WHOLESALER_CP_CLASSIFICATION, \n",
      "COUNT(*) - COUNT(TRANSF_WHOLESALER_CORN_CLASSIFICATION) AS TRANSF_COUNT_WHOLESALER_CORN_CLASSIFICATION, \n",
      "COUNT(*) - COUNT(TRANSF_FLAG_INTEGRATION) AS TRANSF_COUNT_FLAG_INTEGRATION, \n",
      "COUNT(*) - COUNT(TRANSF_AMOUNT) AS TRANSF_COUNT_AMOUNT\n",
      "FROM tab1\n",
      "GROUP BY SOURCE_SYSTEM\n"
     ]
    }
   ],
   "source": [
    "print(missing_query)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "metadata": {},
   "outputs": [],
   "source": [
    "string_raw = 'RAW_COUNT_'\n",
    "string_transf = 'TRANSF_COUNT_'\n",
    "\n",
    "raw_list = [ string_raw+x for x in column_names]\n",
    "transf_list = [ string_transf+x for x in column_names]\n",
    "\n",
    "raw_list.insert(0, \"TOTAL\")\n",
    "raw_list.insert(0, \"SOURCE_SYSTEM\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Wall time: 3min 34s\n"
     ]
    }
   ],
   "source": [
    "%%time\n",
    "missing=cursor.execute(missing_query)\n",
    "df_missing = pd.DataFrame(missing.fetchall(), columns=raw_list+transf_list)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "metadata": {
    "scrolled": false
   },
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>SOURCE_SYSTEM</th>\n",
       "      <th>TOTAL</th>\n",
       "      <th>RAW_COUNT_OPERATION</th>\n",
       "      <th>RAW_COUNT_SOURCE_SYSTEM</th>\n",
       "      <th>RAW_COUNT_SALES_REGION</th>\n",
       "      <th>RAW_COUNT_CROP_YEAR</th>\n",
       "      <th>RAW_COUNT_COUNTRY</th>\n",
       "      <th>RAW_COUNT_PARTNER_ROOT_ID</th>\n",
       "      <th>RAW_COUNT_PARTNER_NR_CNPJ</th>\n",
       "      <th>RAW_COUNT_ACCNT_STATE</th>\n",
       "      <th>RAW_COUNT_ACCNT_CITY_NAME</th>\n",
       "      <th>RAW_COUNT_ACCNT_CITY_CODE</th>\n",
       "      <th>RAW_COUNT_ACCNT_NAME</th>\n",
       "      <th>RAW_COUNT_ACCNT_ROOT_ID</th>\n",
       "      <th>RAW_COUNT_ACCNT_CD_DOCUMENT</th>\n",
       "      <th>RAW_COUNT_ACCNT_TYPE</th>\n",
       "      <th>RAW_COUNT_ACCNT_SUBTYPE</th>\n",
       "      <th>RAW_COUNT_ACCNT_SUBTYPE_ORI</th>\n",
       "      <th>RAW_COUNT_ACCNT_TELEPHONE1</th>\n",
       "      <th>RAW_COUNT_ACCNT_TELEPHONE2</th>\n",
       "      <th>RAW_COUNT_ACCNT_EMAIL</th>\n",
       "      <th>RAW_COUNT_NM_BUSINESS_GROUP</th>\n",
       "      <th>RAW_COUNT_NM_BUSINESS_UNIT</th>\n",
       "      <th>RAW_COUNT_PRODUCT_BRAND</th>\n",
       "      <th>RAW_COUNT_ACCNT_GROUP_CD_DOCUMENT</th>\n",
       "      <th>RAW_COUNT_ACCNT_GROUP_NAME</th>\n",
       "      <th>RAW_COUNT_PARTNER_GROUP_CD_DOCUMENT</th>\n",
       "      <th>RAW_COUNT_PARTNER_GROUP_NAME</th>\n",
       "      <th>RAW_COUNT_LOYALTY_MON_1_1</th>\n",
       "      <th>RAW_COUNT_LOYALTY_ELEITOS</th>\n",
       "      <th>RAW_COUNT_LOYALTY_GDI</th>\n",
       "      <th>RAW_COUNT_LOYALTY_KAM</th>\n",
       "      <th>RAW_COUNT_LOYALTY_IMPULSO</th>\n",
       "      <th>RAW_COUNT_LOYALTY_CLIMATE</th>\n",
       "      <th>RAW_COUNT_TIERS_NUMBERS</th>\n",
       "      <th>RAW_COUNT_FLAG_QION_LIMITATION</th>\n",
       "      <th>RAW_COUNT_PARTNER_CP_CLASSIFICATION</th>\n",
       "      <th>RAW_COUNT_PARTNER_CORN_CLASSIFICATION</th>\n",
       "      <th>RAW_COUNT_WHOLESALER_CP_CLASSIFICATION</th>\n",
       "      <th>RAW_COUNT_WHOLESALER_CORN_CLASSIFICATION</th>\n",
       "      <th>RAW_COUNT_FLAG_INTEGRATION</th>\n",
       "      <th>RAW_COUNT_AMOUNT</th>\n",
       "      <th>TRANSF_COUNT_OPERATION</th>\n",
       "      <th>TRANSF_COUNT_SOURCE_SYSTEM</th>\n",
       "      <th>TRANSF_COUNT_SALES_REGION</th>\n",
       "      <th>TRANSF_COUNT_CROP_YEAR</th>\n",
       "      <th>TRANSF_COUNT_COUNTRY</th>\n",
       "      <th>TRANSF_COUNT_PARTNER_ROOT_ID</th>\n",
       "      <th>TRANSF_COUNT_PARTNER_NR_CNPJ</th>\n",
       "      <th>TRANSF_COUNT_ACCNT_STATE</th>\n",
       "      <th>TRANSF_COUNT_ACCNT_CITY_NAME</th>\n",
       "      <th>TRANSF_COUNT_ACCNT_CITY_CODE</th>\n",
       "      <th>TRANSF_COUNT_ACCNT_NAME</th>\n",
       "      <th>TRANSF_COUNT_ACCNT_ROOT_ID</th>\n",
       "      <th>TRANSF_COUNT_ACCNT_CD_DOCUMENT</th>\n",
       "      <th>TRANSF_COUNT_ACCNT_TYPE</th>\n",
       "      <th>TRANSF_COUNT_ACCNT_SUBTYPE</th>\n",
       "      <th>TRANSF_COUNT_ACCNT_SUBTYPE_ORI</th>\n",
       "      <th>TRANSF_COUNT_ACCNT_TELEPHONE1</th>\n",
       "      <th>TRANSF_COUNT_ACCNT_TELEPHONE2</th>\n",
       "      <th>TRANSF_COUNT_ACCNT_EMAIL</th>\n",
       "      <th>TRANSF_COUNT_NM_BUSINESS_GROUP</th>\n",
       "      <th>TRANSF_COUNT_NM_BUSINESS_UNIT</th>\n",
       "      <th>TRANSF_COUNT_PRODUCT_BRAND</th>\n",
       "      <th>TRANSF_COUNT_ACCNT_GROUP_CD_DOCUMENT</th>\n",
       "      <th>TRANSF_COUNT_ACCNT_GROUP_NAME</th>\n",
       "      <th>TRANSF_COUNT_PARTNER_GROUP_CD_DOCUMENT</th>\n",
       "      <th>TRANSF_COUNT_PARTNER_GROUP_NAME</th>\n",
       "      <th>TRANSF_COUNT_LOYALTY_MON_1_1</th>\n",
       "      <th>TRANSF_COUNT_LOYALTY_ELEITOS</th>\n",
       "      <th>TRANSF_COUNT_LOYALTY_GDI</th>\n",
       "      <th>TRANSF_COUNT_LOYALTY_KAM</th>\n",
       "      <th>TRANSF_COUNT_LOYALTY_IMPULSO</th>\n",
       "      <th>TRANSF_COUNT_LOYALTY_CLIMATE</th>\n",
       "      <th>TRANSF_COUNT_TIERS_NUMBERS</th>\n",
       "      <th>TRANSF_COUNT_FLAG_QION_LIMITATION</th>\n",
       "      <th>TRANSF_COUNT_PARTNER_CP_CLASSIFICATION</th>\n",
       "      <th>TRANSF_COUNT_PARTNER_CORN_CLASSIFICATION</th>\n",
       "      <th>TRANSF_COUNT_WHOLESALER_CP_CLASSIFICATION</th>\n",
       "      <th>TRANSF_COUNT_WHOLESALER_CORN_CLASSIFICATION</th>\n",
       "      <th>TRANSF_COUNT_FLAG_INTEGRATION</th>\n",
       "      <th>TRANSF_COUNT_AMOUNT</th>\n",
       "    </tr>\n",