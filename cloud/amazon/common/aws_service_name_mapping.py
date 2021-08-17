from meta.config_meta import FinalConfigMeta
from types_extensions import safe_type


class AWSServiceNameMapping(metaclass=FinalConfigMeta):

    ACCESSANALYZER: safe_type(str) = 'accessanalyzer'
    ACM: safe_type(str) = 'acm'
    ACM_PCA: safe_type(str) = 'acm-pca'
    ALEXAFORBUSINESS: safe_type(str) = 'alexaforbusiness'
    AMP: safe_type(str) = 'amp'
    AMPLIFY: safe_type(str) = 'amplify'
    AMPLIFYBACKEND: safe_type(str) = 'amplifybackend'
    APIGATEWAY: safe_type(str) = 'apigateway'
    APIGATEWAYMANAGEMENTAPI: safe_type(str) = 'apigatewaymanagementapi'
    APIGATEWAYV2: safe_type(str) = 'apigatewayv2'
    APPCONFIG: safe_type(str) = 'appconfig'
    APPFLOW: safe_type(str) = 'appflow'
    APPINTEGRATIONS: safe_type(str) = 'appintegrations'
    APPLICATION_AUTOSCALING: safe_type(str) = 'application-autoscaling'
    APPLICATION_INSIGHTS: safe_type(str) = 'application-insights'
    APPLICATIONCOSTPROFILER: safe_type(str) = 'applicationcostprofiler'
    APPMESH: safe_type(str) = 'appmesh'
    APPRUNNER: safe_type(str) = 'apprunner'
    APPSTREAM: safe_type(str) = 'appstream'
    APPSYNC: safe_type(str) = 'appsync'
    ATHENA: safe_type(str) = 'athena'
    AUDITMANAGER: safe_type(str) = 'auditmanager'
    AUTOSCALING: safe_type(str) = 'autoscaling'
    AUTOSCALING_PLANS: safe_type(str) = 'autoscaling-plans'
    BACKUP: safe_type(str) = 'backup'
    BATCH: safe_type(str) = 'batch'
    BRAKET: safe_type(str) = 'braket'
    BUDGETS: safe_type(str) = 'budgets'
    CE: safe_type(str) = 'ce'
    CHIME: safe_type(str) = 'chime'
    CHIME_SDK_IDENTITY: safe_type(str) = 'chime-sdk-identity'
    CHIME_SDK_MESSAGING: safe_type(str) = 'chime-sdk-messaging'
    CLOUD9: safe_type(str) = 'cloud9'
    CLOUDDIRECTORY: safe_type(str) = 'clouddirectory'
    CLOUDFORMATION: safe_type(str) = 'cloudformation'
    CLOUDFRONT: safe_type(str) = 'cloudfront'
    CLOUDHSM: safe_type(str) = 'cloudhsm'
    CLOUDHSMV2: safe_type(str) = 'cloudhsmv2'
    CLOUDSEARCH: safe_type(str) = 'cloudsearch'
    CLOUDSEARCHDOMAIN: safe_type(str) = 'cloudsearchdomain'
    CLOUDTRAIL: safe_type(str) = 'cloudtrail'
    CLOUDWATCH: safe_type(str) = 'cloudwatch'
    CODEARTIFACT: safe_type(str) = 'codeartifact'
    CODEBUILD: safe_type(str) = 'codebuild'
    CODECOMMIT: safe_type(str) = 'codecommit'
    CODEDEPLOY: safe_type(str) = 'codedeploy'
    CODEGURU_REVIEWER: safe_type(str) = 'codeguru-reviewer'
    CODEGURUPROFILER: safe_type(str) = 'codeguruprofiler'
    CODEPIPELINE: safe_type(str) = 'codepipeline'
    CODESTAR: safe_type(str) = 'codestar'
    CODESTAR_CONNECTIONS: safe_type(str) = 'codestar-connections'
    CODESTAR_NOTIFICATIONS: safe_type(str) = 'codestar-notifications'
    COGNITO_IDENTITY: safe_type(str) = 'cognito-identity'
    COGNITO_IDP: safe_type(str) = 'cognito-idp'
    COGNITO_SYNC: safe_type(str) = 'cognito-sync'
    COMPREHEND: safe_type(str) = 'comprehend'
    COMPREHENDMEDICAL: safe_type(str) = 'comprehendmedical'
    COMPUTE_OPTIMIZER: safe_type(str) = 'compute-optimizer'
    CONFIG: safe_type(str) = 'config'
    CONNECT: safe_type(str) = 'connect'
    CONNECT_CONTACT_LENS: safe_type(str) = 'connect-contact-lens'
    CONNECTPARTICIPANT: safe_type(str) = 'connectparticipant'
    CUR: safe_type(str) = 'cur'
    CUSTOMER_PROFILES: safe_type(str) = 'customer-profiles'
    DATABREW: safe_type(str) = 'databrew'
    DATAEXCHANGE: safe_type(str) = 'dataexchange'
    DATAPIPELINE: safe_type(str) = 'datapipeline'
    DATASYNC: safe_type(str) = 'datasync'
    DAX: safe_type(str) = 'dax'
    DETECTIVE: safe_type(str) = 'detective'
    DEVICEFARM: safe_type(str) = 'devicefarm'
    DEVOPS_GURU: safe_type(str) = 'devops-guru'
    DIRECTCONNECT: safe_type(str) = 'directconnect'
    DISCOVERY: safe_type(str) = 'discovery'
    DLM: safe_type(str) = 'dlm'
    DMS: safe_type(str) = 'dms'
    DOCDB: safe_type(str) = 'docdb'
    DS: safe_type(str) = 'ds'
    DYNAMODB: safe_type(str) = 'dynamodb'
    DYNAMODBSTREAMS: safe_type(str) = 'dynamodbstreams'
    EBS: safe_type(str) = 'ebs'
    EC2: safe_type(str) = 'ec2'
    EC2_INSTANCE_CONNECT: safe_type(str) = 'ec2-instance-connect'
    ECR: safe_type(str) = 'ecr'
    ECR_PUBLIC: safe_type(str) = 'ecr-public'
    ECS: safe_type(str) = 'ecs'
    EFS: safe_type(str) = 'efs'
    EKS: safe_type(str) = 'eks'
    ELASTIC_INFERENCE: safe_type(str) = 'elastic-inference'
    ELASTICACHE: safe_type(str) = 'elasticache'
    ELASTICBEANSTALK: safe_type(str) = 'elasticbeanstalk'
    ELASTICTRANSCODER: safe_type(str) = 'elastictranscoder'
    ELB: safe_type(str) = 'elb'
    ELBV2: safe_type(str) = 'elbv2'
    EMR: safe_type(str) = 'emr'
    EMR_CONTAINERS: safe_type(str) = 'emr-containers'
    ES: safe_type(str) = 'es'
    EVENTS: safe_type(str) = 'events'
    FINSPACE: safe_type(str) = 'finspace'
    FINSPACE_DATA: safe_type(str) = 'finspace-data'
    FIREHOSE: safe_type(str) = 'firehose'
    FIS: safe_type(str) = 'fis'
    FMS: safe_type(str) = 'fms'
    FORECAST: safe_type(str) = 'forecast'
    FORECASTQUERY: safe_type(str) = 'forecastquery'
    FRAUDDETECTOR: safe_type(str) = 'frauddetector'
    FSX: safe_type(str) = 'fsx'
    GAMELIFT: safe_type(str) = 'gamelift'
    GLACIER: safe_type(str) = 'glacier'
    GLOBALACCELERATOR: safe_type(str) = 'globalaccelerator'
    GLUE: safe_type(str) = 'glue'
    GREENGRASS: safe_type(str) = 'greengrass'
    GREENGRASSV2: safe_type(str) = 'greengrassv2'
    GROUNDSTATION: safe_type(str) = 'groundstation'
    GUARDDUTY: safe_type(str) = 'guardduty'
    HEALTH: safe_type(str) = 'health'
    HEALTHLAKE: safe_type(str) = 'healthlake'
    HONEYCODE: safe_type(str) = 'honeycode'
    IAM: safe_type(str) = 'iam'
    IDENTITYSTORE: safe_type(str) = 'identitystore'
    IMAGEBUILDER: safe_type(str) = 'imagebuilder'
    IMPORTEXPORT: safe_type(str) = 'importexport'
    INSPECTOR: safe_type(str) = 'inspector'
    IOT: safe_type(str) = 'iot'
    IOT_DATA: safe_type(str) = 'iot-data'
    IOT_JOBS_DATA: safe_type(str) = 'iot-jobs-data'
    IOT1CLICK_DEVICES: safe_type(str) = 'iot1click-devices'
    IOT1CLICK_PROJECTS: safe_type(str) = 'iot1click-projects'
    IOTANALYTICS: safe_type(str) = 'iotanalytics'
    IOTDEVICEADVISOR: safe_type(str) = 'iotdeviceadvisor'
    IOTEVENTS: safe_type(str) = 'iotevents'
    IOTEVENTS_DATA: safe_type(str) = 'iotevents-data'
    IOTFLEETHUB: safe_type(str) = 'iotfleethub'
    IOTSECURETUNNELING: safe_type(str) = 'iotsecuretunneling'
    IOTSITEWISE: safe_type(str) = 'iotsitewise'
    IOTTHINGSGRAPH: safe_type(str) = 'iotthingsgraph'
    IOTWIRELESS: safe_type(str) = 'iotwireless'
    IVS: safe_type(str) = 'ivs'
    KAFKA: safe_type(str) = 'kafka'
    KENDRA: safe_type(str) = 'kendra'
    KINESIS: safe_type(str) = 'kinesis'
    KINESIS_VIDEO_ARCHIVED_MEDIA: safe_type(str) = 'kinesis-video-archived-media'
    KINESIS_VIDEO_MEDIA: safe_type(str) = 'kinesis-video-media'
    KINESIS_VIDEO_SIGNALING: safe_type(str) = 'kinesis-video-signaling'
    KINESISANALYTICS: safe_type(str) = 'kinesisanalytics'
    KINESISANALYTICSV2: safe_type(str) = 'kinesisanalyticsv2'
    KINESISVIDEO: safe_type(str) = 'kinesisvideo'
    KMS: safe_type(str) = 'kms'
    LAKEFORMATION: safe_type(str) = 'lakeformation'
    LAMBDA: safe_type(str) = 'lambda'
    LEX_MODELS: safe_type(str) = 'lex-models'
    LEX_RUNTIME: safe_type(str) = 'lex-runtime'
    LEXV2_MODELS: safe_type(str) = 'lexv2-models'
    LEXV2_RUNTIME: safe_type(str) = 'lexv2-runtime'
    LICENSE_MANAGER: safe_type(str) = 'license-manager'
    LIGHTSAIL: safe_type(str) = 'lightsail'
    LOCATION: safe_type(str) = 'location'
    LOGS: safe_type(str) = 'logs'
    LOOKOUTEQUIPMENT: safe_type(str) = 'lookoutequipment'
    LOOKOUTMETRICS: safe_type(str) = 'lookoutmetrics'
    LOOKOUTVISION: safe_type(str) = 'lookoutvision'
    MACHINELEARNING: safe_type(str) = 'machinelearning'
    MACIE: safe_type(str) = 'macie'
    MACIE2: safe_type(str) = 'macie2'
    MANAGEDBLOCKCHAIN: safe_type(str) = 'managedblockchain'
    MARKETPLACE_CATALOG: safe_type(str) = 'marketplace-catalog'
    MARKETPLACE_ENTITLEMENT: safe_type(str) = 'marketplace-entitlement'
    MARKETPLACECOMMERCEANALYTICS: safe_type(str) = 'marketplacecommerceanalytics'
    MEDIACONNECT: safe_type(str) = 'mediaconnect'
    MEDIACONVERT: safe_type(str) = 'mediaconvert'
    MEDIALIVE: safe_type(str) = 'medialive'
    MEDIAPACKAGE: safe_type(str) = 'mediapackage'
    MEDIAPACKAGE_VOD: safe_type(str) = 'mediapackage-vod'
    MEDIASTORE: safe_type(str) = 'mediastore'
    MEDIASTORE_DATA: safe_type(str) = 'mediastore-data'
    MEDIATAILOR: safe_type(str) = 'mediatailor'
    METERINGMARKETPLACE: safe_type(str) = 'meteringmarketplace'
    MGH: safe_type(str) = 'mgh'
    MGN: safe_type(str) = 'mgn'
    MIGRATIONHUB_CONFIG: safe_type(str) = 'migrationhub-config'
    MOBILE: safe_type(str) = 'mobile'
    MQ: safe_type(str) = 'mq'
    MTURK: safe_type(str) = 'mturk'
    MWAA: safe_type(str) = 'mwaa'
    NEPTUNE: safe_type(str) = 'neptune'
    NETWORK_FIREWALL: safe_type(str) = 'network-firewall'
    NETWORKMANAGER: safe_type(str) = 'networkmanager'
    NIMBLE: safe_type(str) = 'nimble'
    OPSWORKS: safe_type(str) = 'opsworks'
    OPSWORKSCM: safe_type(str) = 'opsworkscm'
    ORGANIZATIONS: safe_type(str) = 'organizations'
    OUTPOSTS: safe_type(str) = 'outposts'
    PERSONALIZE: safe_type(str) = 'personalize'
    PERSONALIZE_EVENTS: safe_type(str) = 'personalize-events'
    PERSONALIZE_RUNTIME: safe_type(str) = 'personalize-runtime'
    PI: safe_type(str) = 'pi'
    PINPOINT: safe_type(str) = 'pinpoint'
    PINPOINT_EMAIL: safe_type(str) = 'pinpoint-email'
    PINPOINT_SMS_VOICE: safe_type(str) = 'pinpoint-sms-voice'
    POLLY: safe_type(str) = 'polly'
    PRICING: safe_type(str) = 'pricing'
    PROTON: safe_type(str) = 'proton'
    QLDB: safe_type(str) = 'qldb'
    QLDB_SESSION: safe_type(str) = 'qldb-session'
    QUICKSIGHT: safe_type(str) = 'quicksight'
    RAM: safe_type(str) = 'ram'
    RDS: safe_type(str) = 'rds'
    RDS_DATA: safe_type(str) = 'rds-data'
    REDSHIFT: safe_type(str) = 'redshift'
    REDSHIFT_DATA: safe_type(str) = 'redshift-data'
    REKOGNITION: safe_type(str) = 'rekognition'
    RESOURCE_GROUPS: safe_type(str) = 'resource-groups'
    RESOURCEGROUPSTAGGINGAPI: safe_type(str) = 'resourcegroupstaggingapi'
    ROBOMAKER: safe_type(str) = 'robomaker'
    ROUTE53: safe_type(str) = 'route53'
    ROUTE53_RECOVERY_CLUSTER: safe_type(str) = 'route53-recovery-cluster'
    ROUTE53_RECOVERY_CONTROL_CONFIG: safe_type(str) = 'route53-recovery-control-config'
    ROUTE53_RECOVERY_READINESS: safe_type(str) = 'route53-recovery-readiness'
    ROUTE53DOMAINS: safe_type(str) = 'route53domains'
    ROUTE53RESOLVER: safe_type(str) = 'route53resolver'
    S3: safe_type(str) = 's3'
    S3CONTROL: safe_type(str) = 's3control'
    S3OUTPOSTS: safe_type(str) = 's3outposts'
    SAGEMAKER: safe_type(str) = 'sagemaker'
    SAGEMAKER_A2I_RUNTIME: safe_type(str) = 'sagemaker-a2i-runtime'
    SAGEMAKER_EDGE: safe_type(str) = 'sagemaker-edge'
    SAGEMAKER_FEATURESTORE_RUNTIME: safe_type(str) = 'sagemaker-featurestore-runtime'
    SAGEMAKER_RUNTIME: safe_type(str) = 'sagemaker-runtime'
    SAVINGSPLANS: safe_type(str) = 'savingsplans'
    SCHEMAS: safe_type(str) = 'schemas'
    SDB: safe_type(str) = 'sdb'
    SECRETSMANAGER: safe_type(str) = 'secretsmanager'
    SECURITYHUB: safe_type(str) = 'securityhub'
    SERVERLESSREPO: safe_type(str) = 'serverlessrepo'
    SERVICE_QUOTAS: safe_type(str) = 'service-quotas'
    SERVICECATALOG: safe_type(str) = 'servicecatalog'
    SERVICECATALOG_APPREGISTRY: safe_type(str) = 'servicecatalog-appregistry'
    SERVICEDISCOVERY: safe_type(str) = 'servicediscovery'
    SES: safe_type(str) = 'ses'
    SESV2: safe_type(str) = 'sesv2'
    SHIELD: safe_type(str) = 'shield'
    SIGNER: safe_type(str) = 'signer'
    SMS: safe_type(str) = 'sms'
    SMS_VOICE: safe_type(str) = 'sms-voice'
    SNOW_DEVICE_MANAGEMENT: safe_type(str) = 'snow-device-management'
    SNOWBALL: safe_type(str) = 'snowball'
    SNS: safe_type(str) = 'sns'
    SQS: safe_type(str) = 'sqs'
    SSM: safe_type(str) = 'ssm'
    SSM_CONTACTS: safe_type(str) = 'ssm-contacts'
    SSM_INCIDENTS: safe_type(str) = 'ssm-incidents'
    SSO: safe_type(str) = 'sso'
    SSO_ADMIN: safe_type(str) = 'sso-admin'
    SSO_OIDC: safe_type(str) = 'sso-oidc'
    STEPFUNCTIONS: safe_type(str) = 'stepfunctions'
    STORAGEGATEWAY: safe_type(str) = 'storagegateway'
    STS: safe_type(str) = 'sts'
    SUPPORT: safe_type(str) = 'support'
    SWF: safe_type(str) = 'swf'
    SYNTHETICS: safe_type(str) = 'synthetics'
    TEXTRACT: safe_type(str) = 'textract'
    TIMESTREAM_QUERY: safe_type(str) = 'timestream-query'
    TIMESTREAM_WRITE: safe_type(str) = 'timestream-write'
    TRANSCRIBE: safe_type(str) = 'transcribe'
    TRANSFER: safe_type(str) = 'transfer'
    TRANSLATE: safe_type(str) = 'translate'
    WAF: safe_type(str) = 'waf'
    WAF_REGIONAL: safe_type(str) = 'waf-regional'
    WAFV2: safe_type(str) = 'wafv2'
    WELLARCHITECTED: safe_type(str) = 'wellarchitected'
    WORKDOCS: safe_type(str) = 'workdocs'
    WORKLINK: safe_type(str) = 'worklink'
    WORKMAIL: safe_type(str) = 'workmail'
    WORKMAILMESSAGEFLOW: safe_type(str) = 'workmailmessageflow'
    WORKSPACES: safe_type(str) = 'workspaces'
    XRAY: safe_type(str) = 'xray'