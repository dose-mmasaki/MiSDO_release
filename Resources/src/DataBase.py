import sqlite3


class WriteDB():
    def __init__(self, MODALITY: str, is_dev):
        self.MODALITY = MODALITY
        if is_dev:
            self.DBNAME = 'C:/Users/pudu7o39/source/repos/DoNuTS_dotNET4_0/Resources/MiSDO.db'
        else:
            self.DBNAME = './Resources/MiSDO.db'
        self.MODALITY = MODALITY

        self.conn = sqlite3.connect(self.DBNAME)
        self.cursor = self.conn.cursor()

        if self.MODALITY == 'CT':
            self.cursor.execute("CREATE TABLE IF NOT EXISTS " + 'CT' +
                                """
                                (
                                    PRIMARY_KEY TEXT NOT NULL PRIMARY KEY,
                                    WrittenDate TEXT NOT NULL,
                                    Path TEXT NOT NULL,
                                    Identified_Modality TEXT NOT NULL,
                                    SOPInstanceUID TEXT NULL,
                                    StudyID TEXT NULL,
                                    ManufacturerModelName TEXT NULL ,
                                    PatientID TEXT NULL ,
                                    StudyDate TEXT NULL ,
                                    PatientName TEXT NULL ,
                                    StudyDescription TEXT NULL ,
                                    PatientBirthDate TEXT NULL ,
                                    PatientSex TEXT NULL ,
                                    PatientAge TEXT NULL ,
                                    PatientSize TEXT NULL ,
                                    PatientWeight TEXT NULL ,
                                    AccessionNumber TEXT NULL ,
                                    MeanCTDIvol TEXT NULL  ,
                                    DLP TEXT NULL  ,
                                    Comment TEXT NULL  ,
                                    XRayModulationType TEXT NULL  ,
                                    CTDIwPhantomType TEXT NULL  ,
                                    Acquisition_Protocol TEXT NULL  ,
                                    TargetRegion TEXT NULL  ,
                                    CTAcquisitionType TEXT NULL  ,
                                    ProcedureContext TEXT NULL  ,
                                    ExposureTime TEXT NULL  ,
                                    ScanningLength TEXT NULL  ,
                                    ExposedRange TEXT NULL  ,
                                    NominalSingleCollimationWidth TEXT NULL  ,
                                    NominalTotalCollimationWidth TEXT NULL  ,
                                    PitchFactor TEXT NULL  ,
                                    IdentificationoftheXRaySource TEXT NULL  ,
                                    KVP TEXT NULL  ,
                                    MaximumXRayTubeCurrent TEXT NULL  ,
                                    MeanXRayTubeCurrent TEXT NULL  ,
                                    ExposureTimeperRotation TEXT NULL  ,
                                    DeviceManufacturer TEXT NULL  ,
                                    DeviceSerialNumber TEXT NULL  ,
                                    DLPNotificationValue TEXT NULL  ,
                                    CTDIvolNotificationValue TEXT NULL  ,
                                    ReasonforProceeding TEXT NULL  ,
                                    CTDoseLengthProductTotal TEXT NULL
                                )
                                """)

        elif self.MODALITY == 'XA':
            self.cursor.execute("CREATE TABLE IF NOT EXISTS " + 'XA' +
                                """
                                (
                                    PRIMARY_KEY TEXT NOT NULL PRIMARY KEY,
                                    WrittenDate TEXT NOT NULL,
                                    Path TEXT NOT NULL,
                                    Identified_Modality TEXT NOT NULL,
                                    SOPInstanceUID TEXT NULL,
                                    StudyID TEXT NULL,
                                    ManufacturerModelName TEXT NULL ,
                                    PatientID TEXT NULL ,
                                    StudyDate TEXT NULL ,
                                    PatientName TEXT NULL ,
                                    StudyDescription TEXT NULL ,
                                    PatientBirthDate TEXT NULL ,
                                    PatientSex TEXT NULL ,
                                    PatientAge TEXT NULL ,
                                    PatientSize TEXT NULL ,
                                    PatientWeight TEXT NULL ,
                                    AccessionNumber TEXT NULL ,
                                    Projection_X_Ray TEXT NULL  ,
                                    Irradiation_Event_X_Ray_Data TEXT NULL  ,
                                    Acquisition_Plane TEXT NULL  ,
                                    Irradiation_Event Type TEXT NULL  ,
                                    Acquisition_Protocol TEXT NULL  ,
                                    Reference_Point_Definition TEXT NULL  ,
                                    Dose_Area_Product TEXT NULL  ,
                                    Dose__RP_ TEXT NULL  ,
                                    Collimated_Field_Area TEXT NULL  ,
                                    Positioner_Primary_Angle TEXT NULL  ,
                                    Positioner_Secondary_Angle TEXT NULL  ,
                                    Distance_Source_to_Detector TEXT NULL  ,
                                    Table_Longitudinal_Position TEXT NULL  ,
                                    Table_Lateral_Position TEXT NULL  ,
                                    Table_Height_Position TEXT NULL  ,
                                    KVP TEXT NULL  ,
                                    X_Ray_Tube_Current TEXT NULL  ,
                                    Focal_Spot_Size TEXT NULL 
                                )
                                """)

        elif self.MODALITY in ['PT', 'NM']:
            if self.MODALITY == 'PT':
                table = 'PT'
            else:
                table = 'NM'
            self.cursor.execute("CREATE TABLE IF NOT EXISTS " + table +
                                """
                                (
                                    PRIMARY_KEY TEXT NOT NULL PRIMARY KEY,
                                    WrittenDate TEXT NOT NULL,
                                    Path TEXT NOT NULL,
                                    Identified_Modality TEXT NOT NULL,
                                    SOPInstanceUID TEXT NULL,
                                    StudyID TEXT NULL,
                                    ManufacturerModelName TEXT NULL ,
                                    PatientID TEXT NULL ,
                                    StudyDate TEXT NULL ,
                                    PatientName TEXT NULL ,
                                    StudyDescription TEXT NULL ,
                                    PatientBirthDate TEXT NULL ,
                                    PatientSex TEXT NULL ,
                                    PatientAge TEXT NULL ,
                                    PatientSize TEXT NULL ,
                                    PatientWeight TEXT NULL ,
                                    AccessionNumber TEXT NULL ,
                                    MeanCTDIvol TEXT NULL  ,
                                    DLP TEXT NULL  ,
                                    Comment TEXT NULL  ,
                                    XRayModulationType TEXT NULL  ,
                                    CTDIwPhantomType TEXT NULL  ,
                                    Acquisition_Protocol TEXT NULL  ,
                                    TargetRegion TEXT NULL  ,
                                    CTAcquisitionType TEXT NULL  ,
                                    ProcedureContext TEXT NULL  ,
                                    ExposureTime TEXT NULL  ,
                                    ScanningLength TEXT NULL  ,
                                    ExposedRange TEXT NULL  ,
                                    NominalSingleCollimationWidth TEXT NULL  ,
                                    NominalTotalCollimationWidth TEXT NULL  ,
                                    PitchFactor TEXT NULL  ,
                                    IdentificationoftheXRaySource TEXT NULL  ,
                                    KVP TEXT NULL  ,
                                    MaximumXRayTubeCurrent TEXT NULL  ,
                                    MeanXRayTubeCurrent TEXT NULL  ,
                                    ExposureTimeperRotation TEXT NULL  ,
                                    DeviceManufacturer TEXT NULL  ,
                                    DeviceSerialNumber TEXT NULL  ,
                                    DLPNotificationValue TEXT NULL  ,
                                    CTDIvolNotificationValue TEXT NULL  ,
                                    ReasonforProceeding TEXT NULL  ,
                                    CTDoseLengthProductTotal TEXT NULL,
                                    RadionuclideTotalDose TEXT NULL
                                )
                                """)

        elif self.MODALITY == 'OCR':
            self.cursor.execute("CREATE TABLE IF NOT EXISTS " + 'OCR' +
                                """
                                (
                                    PRIMARY_KEY TEXT NOT NULL PRIMARY KEY,
                                    WrittenDate TEXT NOT NULL,
                                    Path TEXT NOT NULL,
                                    Identified_Modality TEXT NOT NULL,
                                    SOPInstanceUID TEXT NULL,
                                    StudyID TEXT NULL,
                                    ManufacturerModelName TEXT NULL ,
                                    PatientID TEXT NULL ,
                                    StudyDate TEXT NULL ,
                                    PatientName TEXT NULL ,
                                    StudyDescription TEXT NULL ,
                                    PatientBirthDate TEXT NULL ,
                                    PatientSex TEXT NULL ,
                                    PatientAge TEXT NULL ,
                                    PatientSize TEXT NULL ,
                                    PatientWeight TEXT NULL ,
                                    AccessionNumber TEXT NULL ,
                                    Acquisition_Protocol TEXT NULL,
                                    CTAcquisitionType TEXT NULL,
                                    TotalMAS TEXT NULL,
                                    ExposureTime TEXT NULL,
                                    MeanCTDIvol TEXT NULL,
                                    DLP TEXT NULL
                                )
                                """)

        elif self.MODALITY == "ALL_DATA":
            self.cursor.execute("CREATE TABLE IF NOT EXISTS " + "ALL_DATA" +
                                """
                                (
                                    PRIMARY_KEY TEXT NOT NULL PRIMARY KEY,
                                    Runtime TEXT NOT NULL,
                                    Path TEXT NOT NULL,
                                    Identified_Modality TEXT NOT NULL,
                                    SOPInstanceUID TEXT NULL,
                                    StudyInstanceUID TEXT NULL,
                                    StudyID TEXT NULL,
                                    ManufacturerModelName TEXT NULL ,
                                    PatientID TEXT NULL ,
                                    StudyDate TEXT NULL ,
                                    PatientName TEXT NULL ,
                                    StudyDescription TEXT NULL ,
                                    PatientBirthDate TEXT NULL ,
                                    PatientSex TEXT NULL ,
                                    PatientAge TEXT NULL ,
                                    PatientSize TEXT NULL ,
                                    PatientWeight TEXT NULL ,
                                    AccessionNumber TEXT NULL ,
                                    Projection_X_Ray TEXT NULL  ,
                                    Irradiation_Event_X_Ray_Data TEXT NULL  ,
                                    Acquisition_Plane TEXT NULL  ,
                                    Irradiation_Event_Type TEXT NULL  ,
                                    Acquisition_Protocol TEXT NULL  ,
                                    Reference_Point_Definition TEXT NULL  ,
                                    Dose_Area_Product TEXT NULL  ,
                                    Dose__RP_ TEXT NULL  ,
                                    Collimated_Field_Area TEXT NULL  ,
                                    Positioner_Primary_Angle TEXT NULL  ,
                                    Positioner_Secondary_Angle TEXT NULL  ,
                                    Distance_Source_to_Detector TEXT NULL  ,
                                    Table_Longitudinal_Position TEXT NULL  ,
                                    Table_Lateral_Position TEXT NULL  ,
                                    Table_Height_Position TEXT NULL  ,
                                    KVP TEXT NULL  ,
                                    X_Ray_Tube_Current TEXT NULL  ,
                                    Focal_Spot_Size TEXT NULL,
                                    MeanCTDIvol TEXT NULL  ,
                                    DLP TEXT NULL  ,
                                    Comment TEXT NULL  ,
                                    XRayModulationType TEXT NULL  ,
                                    CTDIwPhantomType TEXT NULL  ,
                                    TargetRegion TEXT NULL  ,
                                    CTAcquisitionType TEXT NULL  ,
                                    ProcedureContext TEXT NULL  ,
                                    ExposureTime TEXT NULL  ,
                                    ScanningLength TEXT NULL  ,
                                    ExposedRange TEXT NULL  ,
                                    NominalSingleCollimationWidth TEXT NULL  ,
                                    NominalTotalCollimationWidth TEXT NULL  ,
                                    PitchFactor TEXT NULL  ,
                                    IdentificationoftheXRaySource TEXT NULL  ,
                                    MaximumXRayTubeCurrent TEXT NULL  ,
                                    MeanXRayTubeCurrent TEXT NULL  ,
                                    ExposureTimeperRotation TEXT NULL  ,
                                    DeviceManufacturer TEXT NULL  ,
                                    DeviceSerialNumber TEXT NULL  ,
                                    DLPNotificationValue TEXT NULL  ,
                                    CTDIvolNotificationValue TEXT NULL  ,
                                    ReasonforProceeding TEXT NULL  ,
                                    CTDoseLengthProductTotal TEXT NULL,
                                    RadionuclideTotalDose TEXT NULL,
                                    TotalMAS TEXT NULL
                                )
                                """)

    def insertdb(self, data):
        # column名をlistとして取得
        table = self.MODALITY
        table_cursor = self.conn.execute('SELECT * FROM ' + table)
        names = list(map(lambda x: x[0], table_cursor.description))

        # データを挿入するためのタプルを作成 (?,?,?,...)
        t = ['']

        #  (?,?,?,?,.....,?)を作成する
        for i in range(len(names)):
            if i == 0:
                txt = '?'
            else:
                txt = ',?'
            t[0] += txt
        # tu = tuple(t)
        # tu = '(' + tu[0] + ')'
        tu = '(' + t[0] + ')'

        sql = "INSERT INTO " + self.MODALITY + " VALUES " + tu
        data = tuple(data)
        self.conn.execute(sql, data)
        self.conn.commit()

    def main(self, data: list):
        self.insertdb(data=data)

    def query(self, column: str, key: str):
        cursor = self.conn.cursor()
        sql = "select PRIMARY_KEY, Identified_Modality, RadionuclideTotalDose from ALL_DATA where " + \
            column + "='" + key + "'"
        cursor.execute(sql)
        value_list = cursor.fetchall()
        return value_list
    
    def queryAll(self, column: str, key: str):
        cursor = self.conn.cursor()
        sql = "select * from ALL_DATA where " + \
            column + "='" + key + "'"
        cursor.execute(sql)
        value_list = cursor.fetchall()
        return value_list

    def update(self, id: str, modality:str, dose:str):
        cursor = self.conn.cursor()
        sql = "UPDATE ALL_DATA SET Identified_Modality='" + modality + "', RadionuclideTotalDose='" + dose + "' WHERE PRIMARY_KEY='" + id + "'"
        
        cursor.execute(sql)
        self.conn.commit()

    def close(self):
        self.conn.close()
