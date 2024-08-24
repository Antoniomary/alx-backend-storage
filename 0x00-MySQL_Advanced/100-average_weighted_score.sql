-- creates a stored procedure ComputeAverageWeightedScoreForUser.
-- It computes and store the average weighted score for a student.

DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;

DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
  DECLARE total_weight INT;
  DECLARE total_score_weight INT;

  SELECT SUM(weight) INTO total_weight
    FROM projects;

  SELECT SUM(score * weight) INTO total_score_weight
    FROM corrections
    JOIN projects
    ON corrections.project_id = projects.id
    WHERE corrections.user_id = user_id;

  UPDATE users
  SET average_score = total_score_weight / total_weight
  WHERE id = user_id;
END //

DELIMITER ;
