-- DELIMITER $$
-- 
-- CREATE TRIGGER update_result_participants_on_insert
-- AFTER INSERT ON competition_eventresult
-- FOR EACH ROW
-- BEGIN
--     -- Đếm lại số participants cho result_id
--     UPDATE competition_result
--     SET result_participants = (
--         SELECT COUNT(*)
--         FROM competition_eventresult
--         WHERE result_id_id = NEW.result_id_id
--     )
--     WHERE result_id = NEW.result_id_id;
-- END$$
-- 
-- CREATE TRIGGER update_result_participants_on_delete
-- AFTER DELETE ON competition_eventresult
-- FOR EACH ROW
-- BEGIN
--     -- Đếm lại số participants cho result_id
--     UPDATE competition_result
--     SET result_participants = (
--         SELECT COUNT(*)
--         FROM competition_eventresult
--         WHERE result_id_id = OLD.result_id_id
--     )
--     WHERE result_id = OLD.result_id_id;
-- END$$
-- 
-- DELIMITER ;
-- 

-- DELIMITER $$
-- 
-- CREATE TRIGGER update_result_countries_after_insert
-- AFTER INSERT ON competition_eventresult
-- FOR EACH ROW
-- BEGIN
--     DECLARE country_count INT;
--     
--     -- Đếm số quốc gia tham gia cho kết quả cụ thể
--     SELECT COUNT(DISTINCT a.country_noc_id)
--     INTO country_count
--     FROM athlete_athlete_bio a
--     WHERE a.athlete_id = NEW.athlete_id_id;
-- 
--     -- Cập nhật trường result_countries trong bảng competition_result
--     UPDATE competition_result r
--     SET r.result_countries = country_count
--     WHERE r.result_id = NEW.result_id_id;
-- END $$
-- 
-- DELIMITER ;
-- 
-- DELIMITER $$
-- 
-- CREATE TRIGGER update_result_countries_after_delete
-- AFTER DELETE ON competition_eventresult
-- FOR EACH ROW
-- BEGIN
--     DECLARE country_count INT;
--     
--     -- Đếm lại số quốc gia tham gia cho kết quả cụ thể sau khi xóa
--     SELECT COUNT(DISTINCT a.country_noc_id)
--     INTO country_count
--     FROM athlete_athlete_bio a
--     JOIN competition_eventresult e ON a.athlete_id = e.athlete_id_id
--     WHERE e.result_id_id = OLD.result_id_id;
-- 
--     -- Cập nhật lại trường result_countries trong bảng competition_result
--     UPDATE competition_result r
--     SET r.result_countries = country_count
--     WHERE r.result_id = OLD.result_id_id;
-- END $$
-- 
-- DELIMITER ;
-- 
-- DELIMITER $$
-- 
-- CREATE TRIGGER update_result_countries_after_update
-- AFTER UPDATE ON competition_eventresult
-- FOR EACH ROW
-- BEGIN
--     DECLARE country_count INT;
--     
--     -- Đếm lại số quốc gia tham gia cho kết quả cụ thể sau khi sửa
--     SELECT COUNT(DISTINCT a.country_noc_id)
--     INTO country_count
--     FROM athlete_athlete_bio a
--     JOIN competition_eventresult e ON a.athlete_id = e.athlete_id_id
--     WHERE e.result_id_id = NEW.result_id_id;
-- 
--     -- Cập nhật lại trường result_countries trong bảng competition_result
--     UPDATE competition_result r
--     SET r.result_countries = country_count
--     WHERE r.result_id = NEW.result_id_id;
-- END $$
-- 
-- DELIMITER ;

-- DELIMITER $$
-- 
-- CREATE TRIGGER update_medal_after_insert
-- AFTER INSERT ON competition_medalresult
-- FOR EACH ROW
-- BEGIN
--     -- Tăng số lượng cho loại huy chương mới
--     IF NEW.medal = "Gold" THEN 
--         UPDATE competition_medaltable cm
--         JOIN athlete_athlete_bio a ON NEW.athlete_id_id = a.athlete_id
--         JOIN competition_result r ON NEW.result_id_id = r.result_id
--         SET cm.gold = cm.gold + 1 AND cm.total = cm.total + 1
--         WHERE cm.country_noc_id = a.country_noc_id AND cm.result_id_id = r.result_id;
-- 
--     ELSEIF NEW.medal = "Silver" THEN 
--         UPDATE competition_medaltable cm
--         JOIN athlete_athlete_bio a ON NEW.athlete_id_id = a.athlete_id
--         JOIN competition_result r ON NEW.result_id_id = r.result_id
--         SET cm.silver = cm.silver + 1 AND cm.total = cm.total + 1
--         WHERE cm.country_noc_id = a.country_noc_id AND cm.result_id_id = r.result_id;
-- 
--     ELSEIF NEW.medal = "Bronze" THEN 
--         UPDATE competition_medaltable cm
--         JOIN athlete_athlete_bio a ON NEW.athlete_id_id = a.athlete_id
--         JOIN competition_result r ON NEW.result_id_id = r.result_id
--         SET cm.bronze = cm.bronze + 1 AND cm.total = cm.total + 1
--         WHERE cm.country_noc_id = a.country_noc_id AND cm.result_id_id = r.result_id;
--     END IF;
-- END$$
-- DELIMITER ;

-- DELIMITER $$
-- 
-- CREATE TRIGGER update_medal_after_delete
-- AFTER DELETE ON competition_medalresult
-- FOR EACH ROW
-- BEGIN
--     -- Tăng số lượng cho loại huy chương mới
--     IF OLD.medal = "Gold" THEN 
--         UPDATE competition_medaltable cm
--         JOIN athlete_athlete_bio a ON OLD.athlete_id_id = a.athlete_id
--         JOIN competition_result r ON OLD.result_id_id = r.result_id
--         SET cm.gold = cm.gold - 1 AND cm.total = cm.total - 1
--         WHERE cm.country_noc_id = a.country_noc_id AND cm.result_id_id = r.result_id;
-- 
--     ELSEIF OLD.medal = "Silver" THEN 
--         UPDATE competition_medaltable cm
--         JOIN athlete_athlete_bio a ON OLD.athlete_id_id = a.athlete_id
--         JOIN competition_result r ON OLD.result_id_id = r.result_id
--         SET cm.silver = cm.silver - 1 AND cm.total = cm.total - 1
--         WHERE cm.country_noc_id = a.country_noc_id AND cm.result_id_id = r.result_id;
-- 
--     ELSEIF OLD.medal = "Bronze" THEN 
--         UPDATE competition_medaltable cm
--         JOIN athlete_athlete_bio a ON OLD.athlete_id_id = a.athlete_id
--         JOIN competition_result r ON OLD.result_id_id = r.result_id
--         SET cm.bronze = cm.bronze - 1 AND cm.total = cm.total - 1
--         WHERE cm.country_noc_id = a.country_noc_id AND cm.result_id_id = r.result_id;
--     END IF;
-- END$$
-- DELIMITER ;

DELIMITER $$

CREATE TRIGGER update_medal_after_update
AFTER UPDATE ON competition_medalresult
FOR EACH ROW
BEGIN
    -- Tăng số lượng cho loại huy chương mới
    IF OLD.medal = "Gold" THEN 
        UPDATE competition_medaltable cm
        JOIN athlete_athlete_bio a ON OLD.athlete_id_id = a.athlete_id
        JOIN competition_result r ON OLD.result_id_id = r.result_id
        SET cm.gold = cm.gold - 1
        WHERE cm.country_noc_id = a.country_noc_id AND cm.result_id_id = r.result_id;

    ELSEIF OLD.medal = "Silver" THEN 
        UPDATE competition_medaltable cm
        JOIN athlete_athlete_bio a ON OLD.athlete_id_id = a.athlete_id
        JOIN competition_result r ON OLD.result_id_id = r.result_id
        SET cm.silver = cm.silver - 1
        WHERE cm.country_noc_id = a.country_noc_id AND cm.result_id_id = r.result_id;

    ELSEIF OLD.medal = "Bronze" THEN 
        UPDATE competition_medaltable cm
        JOIN athlete_athlete_bio a ON OLD.athlete_id_id = a.athlete_id
        JOIN competition_result r ON OLD.result_id_id = r.result_id
        SET cm.bronze = cm.bronze - 1
        WHERE cm.country_noc_id = a.country_noc_id AND cm.result_id_id = r.result_id;
    END IF;
    
    IF NEW.medal = "Gold" THEN 
        UPDATE competition_medaltable cm
        JOIN athlete_athlete_bio a ON NEW.athlete_id_id = a.athlete_id
        JOIN competition_result r ON NEW.result_id_id = r.result_id
        SET cm.gold = cm.gold + 1 AND cm.total = cm.total + 1
        WHERE cm.country_noc_id = a.country_noc_id AND cm.result_id_id = r.result_id;

    ELSEIF NEW.medal = "Silver" THEN 
        UPDATE competition_medaltable cm
        JOIN athlete_athlete_bio a ON NEW.athlete_id_id = a.athlete_id
        JOIN competition_result r ON NEW.result_id_id = r.result_id
        SET cm.silver = cm.silver + 1 AND cm.total = cm.total + 1
        WHERE cm.country_noc_id = a.country_noc_id AND cm.result_id_id = r.result_id;

    ELSEIF NEW.medal = "Bronze" THEN 
        UPDATE competition_medaltable cm
        JOIN athlete_athlete_bio a ON NEW.athlete_id_id = a.athlete_id
        JOIN competition_result r ON NEW.result_id_id = r.result_id
        SET cm.bronze = cm.bronze + 1 AND cm.total = cm.total + 1
        WHERE cm.country_noc_id = a.country_noc_id AND cm.result_id_id = r.result_id;
    END IF;
END$$
DELIMITER ;

