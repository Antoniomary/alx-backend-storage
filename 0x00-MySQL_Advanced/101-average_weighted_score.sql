-- creates a stored procedure ComputeAverageWeightedScoreForUser.
-- It computes and store the average weighted score for a student.

DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;

DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
  DECLARE user_id INT;
  DECLARE total_weight INT;
  DECLARE total_score_weight INT;

  DECLARE done INT DEFAULT FALSE;
  DECLARE cur CURSOR FOR
    SELECT id FROM users;
  DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

  SELECT SUM(weight) INTO total_weight
    FROM projects;

  OPEN cur;

  read_loop: LOOP
    FETCH cur INTO user_id;
    IF done THEN
      LEAVE read_loop;
    END IF;

    SELECT SUM(score * weight) INTO total_score_weight
      FROM corrections
      JOIN projects
      ON corrections.project_id = projects.id
      WHERE corrections.user_id = user_id;

    UPDATE users
    SET average_score = total_score_weight / total_weight
    WHERE id = user_id;
  END LOOP;

  CLOSE cur;
END //

DELIMITER ;
