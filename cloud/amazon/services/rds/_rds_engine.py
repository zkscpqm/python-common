from meta.config_meta import FinalConfigMeta
from types_extensions import const


class RDSEngine(metaclass=FinalConfigMeta):

    AURORA: const(str) = 'aurora'
    AURORA_MYSQL: const(str) = 'aurora-mysql'
    AURORA_POSTGRESQL: const(str) = 'aurora-postgresql'
    MARIADB: const(str) = 'mariadb'
    MYSQL: const(str) = 'mysql'
    ORACLE_EE: const(str) = 'oracle-ee'
    ORACLE_EE_CDB: const(str) = 'oracle-ee-cdb'
    ORACLE_SE2: const(str) = 'oracle-se2'
    ORACLE_SE2_CDB: const(str) = 'oracle-se2-cdb'
    POSTGRES: const(str) = 'postgres'
    SQLSERVER_EE: const(str) = 'sqlserver-ee'
    SQLSERVER_SE: const(str) = 'sqlserver-se'
    SQLSERVER_EX: const(str) = 'sqlserver-ex'
    SQLSERVER_WEB: const(str) = 'sqlserver-web'
