Title: Kettle ETL Workflow Design Guide
Date: 2016-11-19 00:00:00
Modified: 2016-11-19 00:00:00
Category: Bigdata
Tags: Kettle
Slug: kettle-etl-workflow-design-guide
Authors: YYCrazy

## 作业日志表

作业日志表记录作业的执行状态：作业名称、开始时间、结束时间、运行状态（Running：运行；Completed：完成；Failed：失败）。

    :::sql
    CREATE TABLE
        t_etl_kjb_log
        (
            log_id     INT NOT NULL AUTO_INCREMENT,
            kjb_name   VARCHAR(255) NOT NULL,
            begin_dttm DATETIME DEFAULT '1970-01-01 00:00:00' NOT NULL,
            end_dttm   DATETIME DEFAULT '1970-01-01 00:00:00' NOT NULL,
            status     VARCHAR(10) NOT NULL,
            PRIMARY KEY(log_id)
        )
        ENGINE = InnoDB DEFAULT CHARSET = utf8;

    CREATE VIEW
        v_etl_kjb_log AS
    SELECT
        t1.kjb_name,
        t1.begin_dttm,
        t2.end_dttm,
        t2.status
    FROM
        (
         SELECT
                kjb_name,
                MAX(begin_dttm) AS begin_dttm
           FROM
                t_etl_kjb_log
       GROUP BY
                kjb_name) t1
    INNER JOIN
        t_etl_kjb_log t2
     ON
        t1.kjb_name = t2.kjb_name
        AND t1.begin_dttm = t2.begin_dttm;

## 数据表日志表

数据表日志表记录数据表的更新状态：作业名称、转换名称、数据表名称、开始时间、结束时间、运行状态（Running：运行；Completed：完成；Failed：失败）、更新计数、错误计数。

    :::sql
    CREATE TABLE
        t_etl_tbl_log
        (
            log_id      INT NOT NULL AUTO_INCREMENT,
            kjb_name    VARCHAR(255) NOT NULL,
            ktr_name    VARCHAR(255) NOT NULL,
            tbl_name    VARCHAR(255) NOT NULL,
            begin_dttm  DATETIME DEFAULT '1970-01-01 00:00:00' NOT NULL,
            end_dttm    DATETIME DEFAULT '1970-01-01 00:00:00' NOT NULL,
            status      VARCHAR(10) NOT NULL,
            row_count   INT DEFAULT 0 NOT NULL,
            error_count INT DEFAULT 0 NOT NULL,
            PRIMARY KEY(log_id)
        )
        ENGINE = InnoDB DEFAULT CHARSET = utf8;

    CREATE VIEW
        v_etl_tbl_log AS
    SELECT
        t2.kjb_name,
        t2.ktr_name,
        t1.tbl_name,
        t1.begin_dttm,
        t2.end_dttm,
        t2.status,
        t2.row_count,
        t2.error_count
    FROM
        (
         SELECT
                tbl_name,
                MAX(begin_dttm) AS begin_dttm
           FROM
                t_etl_tbl_log
       GROUP BY
                tbl_name) t1
    INNER JOIN
        t_etl_tbl_log t2
     ON
        t1.tbl_name = t2.tbl_name
        AND t1.begin_dttm = t2.begin_dttm;

## 作业配置表

作业配置表记录作业的配置信息：作业名称、作业类型、启用标识、重试次数。

    :::sql
    CREATE TABLE
        t_etl_kjb_cfg
        (
            cfg_id     INT NOT NULL AUTO_INCREMENT,
            kjb_name   VARCHAR(255) NOT NULL,
            kjb_type   VARCHAR(20) NOT NULL,
            is_enabled CHAR(1) DEFAULT 'N' NOT NULL,
            retries    INT DEFAULT 3 NOT NULL,
            PRIMARY KEY(cfg_id)
        )
        ENGINE = InnoDB DEFAULT CHARSET = utf8;

## 标准工作流

### 转换配置表

转换配置表记录作业中转换的配置信息：作业名称、转换名称、转换路径、数据表名称、启用标识。

    :::sql
    CREATE TABLE
        t_etl_std_ktr_cfg
        (
            cfg_id     INT NOT NULL auto_increment,
            kjb_name   VARCHAR(255) NOT NULL,
            ktr_name   VARCHAR(255) NOT NULL,
            ktr_path   VARCHAR(255) NOT NULL,
            tbl_name   VARCHAR(255) NOT NULL,
            is_enabled CHAR(1) DEFAULT 'N' NOT NULL,
            PRIMARY KEY(cfg_id)
        )
        ENGINE = InnoDB DEFAULT CHARSET = utf8;

### 依赖关系表

依赖关系表记录作业中数据表的依赖关系：目标数据表、来源数据表、来源数据表 ETL 标识。

    :::sql
    CREATE TABLE
        t_etl_std_dep_cfg
        (
            cfg_id          INT NOT NULL AUTO_INCREMENT,
            tbl_to          VARCHAR(255) NOT NULL,
            tbl_from        VARCHAR(255) NOT NULL,
            tbl_from_is_etl CHAR(1) DEFAULT 'N' NOT NULL,
            PRIMARY KEY(cfg_id)
        )
        ENGINE = InnoDB DEFAULT CHARSET = utf8;

    CREATE VIEW
        v_etl_std_dep_cfg AS
    SELECT
        cfg.tbl_to,
        cfg.tbl_from,
        cfg.tbl_from_is_etl,
        IFNULL(tl.end_dttm, STR_TO_DATE('1970-01-01', '%Y-%m-%d')) AS tbl_to_end_dttm,
        IFNULL(tl.status, 'Failed')                                AS tbl_to_status,
        CASE
            WHEN cfg.tbl_from_is_etl = 'Y'
            THEN IFNULL(fl.end_dttm, STR_TO_DATE('1970-01-01', '%Y-%m-%d'))
            ELSE STR_TO_DATE('2099-12-31', '%Y-%m-%d')
        END AS tbl_from_end_dttm,
        CASE
            WHEN cfg.tbl_from_is_etl = 'Y'
            THEN IFNULL(fl.status, 'Failed')
            ELSE 'Completed'
        END AS tbl_from_status
    FROM
        t_etl_std_dep_cfg cfg
    LEFT JOIN
        v_etl_tbl_log tl
     ON
        cfg.tbl_to = tl.tbl_name
    LEFT JOIN
        v_etl_tbl_log fl
     ON
        cfg.tbl_from = fl.tbl_name;

### 流程设计

![kjb_standard_workflow](uploads/kettle-etl-workflow-design-guide/kjb-standard-workflow.png)

**kjb_standard_workflow:**

1. Parameters
    1. 
        - Parameter: KJB_NAME
        - Default value: !@#$%^&*()
2. START
3. kjb_name_is_set
    - Evaluate: Variable
    - Variable name: ${KJB_NAME}
    - Type: String
    - Success condition: If value is different from
    - Value: !@#$%^&*()
4. kjb_is_valid
    1. Table input
        - [X] Replace variables in script
    2. Set Variables
        - [X] Apply formatting
        1. 
            - Field name: is_enabled
            - Variable name: KJB_IS_ENABLED
            - Variable scope type: Valid in the root job
            - Default value: N
        2. 
            - Field name: retries
            - Variable name: MAX_RETRIES
            - Variable scope type: Valid in the root job
5. kjb_is_enabled
    - Evaluate: Variable
    - Variable name: ${KJB_IS_ENABLED}
    - Type: String
    - Success condition: If value is equal to
    - Value: Y
6. kjb_log_initial
    1. Table input
        - [X] Replace variables in script
    2. Table output
        - Target table: t_etl_kjb_log
    3. Set Variables
        - [X] Apply formatting
        1. 
            - Field name: begin_dttm
            - Variable name: KJB_BEGIN_DTTM
            - Variable scope type: Valid in the root job
7. get_ktr_list
    1. Table input
        - [X] Replace variables in script
    2. Copy rows to result
8. exec_ktr
    - [X] Execute for every input row
9. kjb_log_completed
    - [X] Use variable substitution
10. kjb_log_failed
    - [X] Use variable substitution

![exec_ktr](uploads/kettle-etl-workflow-design-guide/kjb-standard-workflow-exec-ktr.png)

**exec_ktr:**

1. START
2. set_ktr_vars
    1. Get rows from result
        1. 
            - Fieldname: ktr_name
            - Type: String
        2. 
            - Fieldname: ktr_path
            - Type: String
        3. 
            - Fieldname: tbl_name
            - Type: String
    2. Set Variables
        - [X] Apply formatting
        1. 
            - Field name: ktr_name
            - Variable name: KTR_NAME
            - Variable scope type: Valid in the root job
        2. 
            - Field name: ktr_path
            - Variable name: KTR_PATH
            - Variable scope type: Valid in the root job
        3. 
            - Field name: tbl_name
            - Variable name: TBL_NAME
            - Variable scope type: Valid in the root job
3. tbl_log_initial
    1. Table input
        - [X] Replace variables in script
    2. Table output
        - Target table: t_etl_tbl_log
    3. Set Variables
        - [X] Apply formatting
        1. 
            - Field name: begin_dttm
            - Variable name: KTR_BEGIN_DTTM
            - Variable scope type: Valid in the root job
4. Transformation
    - [X] Specify by name and directory
        - ${KTR_NAME}
        - ${KTR_PATH}
5. tbl_log_completed
    - [X] Use variable substitution
6. inc_err_cnt
    - [X] Use variable substitution
7. set_err_cnt
    1. Table input
        - [X] Replace variables in script
    2. Set Variables
        - [X] Apply formatting
        1. 
            - Field name: error_count
            - Variable name: ERROR_COUNT
            - Variable scope type: Valid in the root job
8. max_retries
    - Evaluate: Variable
    - Variable name: ${ERROR_COUNT}
    - Type: Number
    - Success condition: If value is greater or equal
    - Value: ${MAX_RETRIES}
9. tbl_log_failed
    - [X] Use variable substitution

#### kjb_standard_workflow

##### kjb_is_valid

    :::sql
    SELECT
        is_enabled,
        retries
    FROM
        t_etl_kjb_cfg
    WHERE
        kjb_name = '${KJB_NAME}'
        AND kjb_type = 'STANDARD'
        AND is_enabled = 'Y';

##### kjb_log_initial

    :::sql
    SELECT
        '${KJB_NAME}' AS kjb_name,
        NOW()         AS begin_dttm,
        'Running'     AS status
    FROM
        dual;

##### get_ktr_list

    :::sql
    SELECT
        cfg.ktr_name,
        cfg.ktr_path,
        cfg.tbl_name
    FROM
        t_etl_std_ktr_cfg cfg
    LEFT JOIN
        v_etl_tbl_log log
     ON
        cfg.tbl_name = log.tbl_name
    WHERE
        cfg.kjb_name = '${KJB_NAME}'
        AND cfg.tbl_name IN
        (
         SELECT
                tbl_to
           FROM
                v_etl_std_dep_cfg
       GROUP BY
                tbl_to
         HAVING
                SUM(
                    CASE
                        WHEN tbl_from_status = 'Completed'
                            AND tbl_from_end_dttm > tbl_to_end_dttm
                        THEN 0
                        ELSE 1
                    END) = 0)
        AND cfg.is_enabled = 'Y'
        AND(
            log.status = 'Failed'
            OR log.end_dttm < CURDATE()
            OR log.end_dttm IS NULL);

##### kjb_log_completed

    :::sql
    UPDATE
        t_etl_kjb_log
    SET
        end_dttm = NOW(),
        status = 'Completed'
    WHERE
        kjb_name = '${KJB_NAME}'
        AND begin_dttm = '${KJB_BEGIN_DTTM}';

##### kjb_log_failed

    :::sql
    UPDATE
        t_etl_kjb_log
    SET
        end_dttm = NOW(),
        status = 'Failed'
    WHERE
        kjb_name = '${KJB_NAME}'
        AND begin_dttm = '${KJB_BEGIN_DTTM}';

#### exec_ktr

##### tbl_log_initial

    :::sql
    SELECT
        '${KJB_NAME}' AS kjb_name,
        '${KTR_NAME}' AS ktr_name,
        '${TBL_NAME}' AS tbl_name,
        NOW()         AS begin_dttm,
        'Running'     AS status
    FROM
        dual;

##### tbl_log_completed

    :::sql
    UPDATE
        t_etl_tbl_log
    SET
        end_dttm = NOW(),
        status = 'Completed',
        row_count = ${ROW_COUNT}
    WHERE
        kjb_name = '${KJB_NAME}'
        AND ktr_name = '${KTR_NAME}'
        AND tbl_name = '${TBL_NAME}'
        AND begin_dttm = '${KTR_BEGIN_DTTM}';

##### inc_err_cnt

    :::sql
    UPDATE
        t_etl_tbl_log
    SET
        error_count = error_count + 1
    WHERE
        kjb_name = '${KJB_NAME}'
        AND ktr_name = '${KTR_NAME}'
        AND tbl_name = '${TBL_NAME}'
        AND begin_dttm = '${KTR_BEGIN_DTTM}';

##### set_err_cnt

    :::sql
    SELECT
        error_count
    FROM
        t_etl_tbl_log
    WHERE
        kjb_name = '${KJB_NAME}'
        AND ktr_name = '${KTR_NAME}'
        AND tbl_name = '${TBL_NAME}'
        AND begin_dttm = '${KTR_BEGIN_DTTM}';

##### tbl_log_failed

    :::sql
    UPDATE
        t_etl_tbl_log
    SET
        end_dttm = NOW(),
        status = 'Failed'
    WHERE
        kjb_name = '${KJB_NAME}'
        AND ktr_name = '${KTR_NAME}'
        AND tbl_name = '${TBL_NAME}'
        AND begin_dttm = '${KTR_BEGIN_DTTM}';

## 运维工作流

### 转换配置表

转换配置表记录作业中转换的配置信息：作业名称、转换名称、转换路径、数据表名称、执行序号、启用标识。

    :::sql
    CREATE TABLE
        t_etl_maint_ktr_cfg
        (
            cfg_id     INT NOT NULL AUTO_INCREMENT,
            kjb_name   VARCHAR(255) NOT NULL,
            ktr_name   VARCHAR(255) NOT NULL,
            ktr_path   VARCHAR(255) NOT NULL,
            tbl_name   VARCHAR(255) NOT NULL,
            is_enabled CHAR(1) DEFAULT 'N' NOT NULL,
            exec_order INT NOT NULL,
            PRIMARY KEY(cfg_id),
            CONSTRAINT unq_kjb_name_exec_order UNIQUE(kjb_name, exec_order)
        )
        ENGINE = InnoDB DEFAULT CHARSET = utf8;

### 流程设计

![kjb_maintenance_workflow](uploads/kettle-etl-workflow-design-guide/kjb-maintenance-workflow.png)

**kjb_maintenance_workflow:**

1. Parameters
    1. 
        - Parameter: KJB_NAME
        - Default value: !@#$%^&*()
2. START
3. kjb_name_is_set
    - Evaluate: Variable
    - Variable name: ${KJB_NAME}
    - Type: String
    - Success condition: If value is different from
    - Value: !@#$%^&*()
4. kjb_is_valid
    1. Table input
        - [X] Replace variables in script
    2. Set Variables
        - [X] Apply formatting
        1. 
            - Field name: is_enabled
            - Variable name: KJB_IS_ENABLED
            - Variable scope type: Valid in the root job
            - Default value: N
        2. 
            - Field name: retries
            - Variable name: MAX_RETRIES
            - Variable scope type: Valid in the root job
5. kjb_is_enabled
    - Evaluate: Variable
    - Variable name: ${KJB_IS_ENABLED}
    - Type: String
    - Success condition: If value is equal to
    - Value: Y
6. kjb_log_initial
    1. Table input
        - [X] Replace variables in script
    2. Table output
        - Target table: t_etl_kjb_log
    3. Set Variables
        - [X] Apply formatting
        1. 
            - Field name: begin_dttm
            - Variable name: KJB_BEGIN_DTTM
            - Variable scope type: Valid in the root job
7. set_default
    - Variables
        1. 
            - Variable name: EXEC_ORDER
            - Value: 0
            - Variable scope type: Valid in the root job
8. exec_ktrs
9. kjb_log_completed
    - [X] Use variable substitution
10. kjb_log_failed
    - [X] Use variable substitution

![exec_ktrs](uploads/kettle-etl-workflow-design-guide/kjb-maintenance-workflow-exec-ktrs.png)

**exec_ktrs:**

1. START
2. set_ktr_vars
    1. Table input
        - [X] Replace variables in script
    2. Set Variables
        - [X] Apply formatting
        1. 
            - Field name: ktr_name
            - Variable name: KTR_NAME
            - Variable scope type: Valid in the root job
            - Default value: !@#$%^&*()
        2. 
            - Field name: ktr_path
            - Variable name: KTR_PATH
            - Variable scope type: Valid in the root job
            - Default value: !@#$%^&*()
        3. 
            - Field name: tbl_name
            - Variable name: TBL_NAME
            - Variable scope type: Valid in the root job
            - Default value: !@#$%^&*()
        4. 
            - Field name: exec_order
            - Variable name: EXEC_ORDER
            - Variable scope type: Valid in the root job
            - Default value: !@#$%^&*()
3. ktr_vars_not_set
    - Evaluate: Variable
    - Variable name: ${EXEC_ORDER}
    - Type: String
    - Success condition: If value is equal to
    - Value: !@#$%^&*()
4. Success
5. tbl_log_initial
    1. Table input
        - [X] Replace variables in script
    2. Table output
        - Target table: t_etl_tbl_log
    3. Set Variables
        - [X] Apply formatting
        1. 
            - Field name: begin_dttm
            - Variable name: KTR_BEGIN_DTTM
            - Variable scope type: Valid in the root job
6. Transformation
    - [X] Specify by name and directory
        - ${KTR_NAME}
        - ${KTR_PATH}
7. tbl_log_completed
    - [X] Use variable substitution
8. inc_err_cnt
    - [X] Use variable substitution
9. set_err_cnt
    1. Table input
        - [X] Replace variables in script
    2. Set Variables
        - [X] Apply formatting
        1. 
            - Field name: error_count
            - Variable name: ERROR_COUNT
            - Variable scope type: Valid in the root job
10. max_retries
    - Evaluate: Variable
    - Variable name: ${ERROR_COUNT}
    - Type: Number
    - Success condition: If value is greater or equal
    - Value: ${MAX_RETRIES}
11. tbl_log_failed
    - [X] Use variable substitution
12. Abort

#### kjb_maintenance_workflow

##### kjb_is_valid

    :::sql
    SELECT
        is_enabled,
        retries
    FROM
        t_etl_kjb_cfg
    WHERE
        kjb_name = '${KJB_NAME}'
        AND kjb_type = 'MAINTENANCE'
        AND is_enabled = 'Y';

##### kjb_log_initial

    :::sql
    SELECT
        '${KJB_NAME}' AS kjb_name,
        NOW()         AS begin_dttm,
        'Running'     AS status
    FROM
        dual;

##### kjb_log_completed

    :::sql
    UPDATE
        t_etl_kjb_log
    SET
        end_dttm = NOW(),
        status = 'Completed'
    WHERE
        kjb_name = '${KJB_NAME}'
        AND begin_dttm = '${KJB_BEGIN_DTTM}';

##### kjb_log_failed

    :::sql
    UPDATE
        t_etl_kjb_log
    SET
        end_dttm = NOW(),
        status = 'Failed'
    WHERE
        kjb_name = '${KJB_NAME}'
        AND begin_dttm = '${KJB_BEGIN_DTTM}';

#### exec_ktrs

##### set_ktr_vars

    :::sql
    SELECT
        ktr_name,
        ktr_path,
        tbl_name,
        exec_order
    FROM
        t_etl_maint_ktr_cfg
    WHERE
        (
            kjb_name, exec_order) =
        (
         SELECT
                kjb_name,
                MIN(exec_order)
           FROM
                t_etl_maint_ktr_cfg
          WHERE
                kjb_name = '${KJB_NAME}'
                AND is_enabled = 'Y'
                AND exec_order > '${EXEC_ORDER}');

##### tbl_log_initial

    :::sql
    SELECT
        '${KJB_NAME}' AS kjb_name,
        '${KTR_NAME}' AS ktr_name,
        '${TBL_NAME}' AS tbl_name,
        NOW()         AS begin_dttm,
        'Running'     AS status
    FROM
        dual;

##### tbl_log_completed

    :::sql
    UPDATE
        t_etl_tbl_log
    SET
        end_dttm = NOW(),
        status = 'Completed',
        row_count = ${ROW_COUNT}
    WHERE
        kjb_name = '${KJB_NAME}'
        AND ktr_name = '${KTR_NAME}'
        AND tbl_name = '${TBL_NAME}'
        AND begin_dttm = '${KTR_BEGIN_DTTM}';

##### inc_err_cnt

    :::sql
    UPDATE
        t_etl_tbl_log
    SET
        error_count = error_count + 1
    WHERE
        kjb_name = '${KJB_NAME}'
        AND ktr_name = '${KTR_NAME}'
        AND tbl_name = '${TBL_NAME}'
        AND begin_dttm = '${KTR_BEGIN_DTTM}';

##### set_err_cnt

    :::sql
    SELECT
        error_count
    FROM
        t_etl_tbl_log
    WHERE
        kjb_name = '${KJB_NAME}'
        AND ktr_name = '${KTR_NAME}'
        AND tbl_name = '${TBL_NAME}'
        AND begin_dttm = '${KTR_BEGIN_DTTM}';

##### tbl_log_failed

    :::sql
    UPDATE
        t_etl_tbl_log
    SET
        end_dttm = NOW(),
        status = 'Failed'
    WHERE
        kjb_name = '${KJB_NAME}'
        AND ktr_name = '${KTR_NAME}'
        AND tbl_name = '${TBL_NAME}'
        AND begin_dttm = '${KTR_BEGIN_DTTM}';

## 转换模板

![Transformation](uploads/kettle-etl-workflow-design-guide/transformation.png)

**Transformation:**

1. Execute SQL script
2. Table input
3. Table output
4. Output steps metrics
    - General
        - Step name: Table output
        - Copy Nr: 0
        - Required: N
    - Fields
        - Lines written: row_count
5. Set Variables
    - [X] Apply formatting
    1. 
        - Field name: row_count
        - Variable name: ROW_COUNT
        - Variable scope type: Valid in the root job
        - Default value: 0
