DROP TABLE IF EXISTS `product`;

CREATE TABLE
    `product` (
        `product_id` int NOT NULL AUTO_INCREMENT,
        `fund_code` VARCHAR(30) DEFAULT NULL,
        `fund_name` VARCHAR(100) DEFAULT NULL,
        `fund_type` VARCHAR(10) DEFAULT NULL,
        `fund_type_description` VARCHAR(50) DEFAULT NULL,
        `fund_sid` VARCHAR(30) DEFAULT NULL,
        `sharia_compliance` VARCHAR(1) DEFAULT NULL,
        `im_code` VARCHAR(7) DEFAULT NULL,
        `im_name` VARCHAR(100) DEFAULT NULL,
        `cb_code` VARCHAR(10) DEFAULT NULL,
        `cb_name` VARCHAR(100) DEFAULT NULL,
        `status` VARCHAR(20) DEFAULT NULL,
        `launching_date` TIMESTAMP DEFAULT NULL,
        `deactivation_date` TIMESTAMP DEFAULT NULL,
        PRIMARY KEY (`product_id`) USING BTREE
    )