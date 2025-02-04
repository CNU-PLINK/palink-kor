-- UTF-8 인코딩 설정
SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;
SET collation_connection = 'utf8mb4_unicode_ci';


-- 데이터베이스 생성
CREATE DATABASE IF NOT EXISTS palink;
USE palink;

-- 기본 설정
SET FOREIGN_KEY_CHECKS=0;

-- ✅ user 테이블 생성
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `user_id` VARCHAR(255) NOT NULL PRIMARY KEY,
  `name` VARCHAR(255),
  `password` VARCHAR(255),
  `age` INT,
  `personality_type` VARCHAR(255)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ✅ character_data (기존 aicharacter 테이블) 생성
DROP TABLE IF EXISTS `character_data`;
CREATE TABLE `character_data` (
  `character_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `ai_name` VARCHAR(255),
  `description` TEXT,
  `difficulty_level` INT
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ✅ conversation 테이블 생성
DROP TABLE IF EXISTS `conversation`;
CREATE TABLE `conversation` (
  `conversation_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `day` DATETIME,
  `user_id` VARCHAR(255),
  `character_id` INT,
  FOREIGN KEY (`user_id`) REFERENCES `user`(`user_id`),
  FOREIGN KEY (`character_id`) REFERENCES `character_data`(`character_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ✅ message 테이블 생성
DROP TABLE IF EXISTS `message`;
CREATE TABLE `message` (
  `message_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `conversation_id` INT,
  `sender` BOOLEAN,
  `message_text` TEXT,
  `timestamp` DATETIME,
  FOREIGN KEY (`conversation_id`) REFERENCES `conversation`(`conversation_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ✅ tip 테이블 생성
DROP TABLE IF EXISTS `tip`;
CREATE TABLE `tip` (
  `tip_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `tip_text` TEXT,
  `message_id` INT,
  FOREIGN KEY (`message_id`) REFERENCES `message`(`message_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ✅ feedback 테이블 생성
DROP TABLE IF EXISTS `feedback`;
CREATE TABLE `feedback` (
  `feedback_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `feedback_text` TEXT,
  `liking_level` INT,
  `day` DATETIME,
  `conversation_id` INT,
  FOREIGN KEY (`conversation_id`) REFERENCES `conversation`(`conversation_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ✅ collection 테이블 생성
DROP TABLE IF EXISTS `collection`;
CREATE TABLE `collection` (
  `collection_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `user_id` VARCHAR(255),
  `character_id` INT,
  `added_date` DATETIME,
  FOREIGN KEY (`user_id`) REFERENCES `user`(`user_id`),
  FOREIGN KEY (`character_id`) REFERENCES `character_data`(`character_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ✅ emotion 테이블 생성
DROP TABLE IF EXISTS `emotion`;
CREATE TABLE `emotion` (
  `emotion_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `emotion_type` VARCHAR(255),
  `vibration_pattern` VARCHAR(255),
  `background_color` VARCHAR(255)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ✅ mindset 테이블 생성
CREATE TABLE `mindset` (
  `mindset_id` int NOT NULL AUTO_INCREMENT,
  `mindset_text` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`mindset_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ✅ liking 테이블 생성
DROP TABLE IF EXISTS `liking`;
CREATE TABLE `liking` (
  `liking_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `user_id` VARCHAR(255),
  `character_id` INT,
  `liking_level` INT,
  `message_id` INT,
  FOREIGN KEY (`user_id`) REFERENCES `user`(`user_id`),
  FOREIGN KEY (`character_id`) REFERENCES `character_data`(`character_id`),
  FOREIGN KEY (`message_id`) REFERENCES `message`(`message_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ✅ rejection 테이블 생성
DROP TABLE IF EXISTS `rejection`;
CREATE TABLE `rejection` (
  `rejection_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `user_id` VARCHAR(255),
  `character_id` INT,
  `rejection_level` INT,
  `message_id` INT,
  FOREIGN KEY (`user_id`) REFERENCES `user`(`user_id`),
  FOREIGN KEY (`character_id`) REFERENCES `character_data`(`character_id`),
  FOREIGN KEY (`message_id`) REFERENCES `message`(`message_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ✅ 초기 데이터 삽입
INSERT INTO mindset (mindset_id, mindset_text) VALUES
(1,'모든 사람을 만족시키려 하면 자신을 잃게 됩니다. 스스로를 우선시하는 것이 중요합니다. 이는 우리의 정신적, 감정적 건강을 지키는 데 필요합니다.'),(2,'사람들 앞에서 말하는 것이 두렵다면, 모두가 처음에는 떨린다는 것을 기억하세요. 반복적인 연습과 작은 성공을 통해 자신감을 키울 수 있습니다.'),(3,'자신감을 키우기 위해서는 자신의 강점을 찾고 그것을 개발하는 것이 중요합니다. 이는 자기 효능감을 높이고 더 나은 자신을 만드는 데 도움이 됩니다.'),(4,'실수는 성장의 과정 중 하나입니다. 실수를 통해 배우고 개선할 수 있습니다. 이를 받아들이면 더 나은 관계를 형성할 수 있습니다.'),(5,'자신을 돌보는 것은 매우 중요합니다. 건강한 마음과 몸이 있어야 다른 사람들과의 관계도 건강하게 유지할 수 있습니다.'),(6,'긍정적인 자기 대화는 자신감을 높이고, 어려운 상황에서도 긍정적인 태도를 유지하는 데 도움이 됩니다. 이는 대인관계에서도 긍정적인 영향을 미칩니다.'),(7,'자신의 생각과 감정을 표현하는 것은 매우 중요합니다. 타인의 반응을 두려워하지 말고 솔직하게 자신을 표현하는 것이 필요합니다. 이는 진정한 나를 보여주고 관계를 깊게 만드는 데 도움이 됩니다.'),(8,'타인의 시선과 평가가 나의 가치를 결정하지 않습니다. 나 자신의 가치와 자존감을 스스로 인정하는 것이 중요합니다. 이는 건강한 자아상을 유지하는 데 도움이 됩니다.'),(9,'과거에 얽매여 현재의 불행한 관계를 유지하는 것은 도움이 되지 않습니다. 과거를 인정하고, 현재와 미래를 위해 필요한 결정을 내리는 것이 중요합니다.'),(10,'내가 편안해야 상대방도 편안해집니다. 나 자신을 \"괜찮다\"고 인정하는 것이 중요합니다.'),(11,'내가 편안한 마음을 가지면, 그 에너지가 상대방에게도 전달됩니다. 이는 자연스럽고 편안한 관계를 형성하는 데 도움이 됩니다.'),(12,'타인의 생각과 의견은 그들의 문제이며, 내가 통제할 수 없는 부분입니다. 나 자신의 감정과 생각에 집중하는 것이 더 중요합니다. 이는 나의 정신적 건강을 지키는 데 도움이 됩니다.'),(13,'타인의 판단은 일시적이고 변할 수 있습니다. 이에 너무 집착하지 말고 나 자신의 길을 가는 것이 중요합니다. 이는 지속적인 자아 발전과 행복을 추구하는 데 도움이 됩니다.'),(14,'모든 사람에게 좋은 인상을 주려고 노력하면 지치게 됩니다. 자신에게 중요한 사람들과의 관계에 집중하는 것이 더 중요합니다. 이는 나의 에너지를 효율적으로 사용하는 데 도움이 됩니다.'),(15,'나의 삶의 주인은 나 자신입니다. 타인의 의견에 휘둘리지 않고, 나의 결정을 스스로 내리는 것이 중요합니다. 이는 진정한 자유와 자아 존중을 이루는 데 도움이 됩니다.'),(16,'우리는 자신의 시간과 에너지를 선택할 권리가 있습니다. 거절은 자신의 필요와 우선순위를 지키기 위한 정당한 선택입니다. 이를 통해 삶을 더 주도적으로 이끌 수 있습니다.'),(17,'갈등 상황에서 상대방을 비난하기보다는 함께 해결책을 찾는 것이 중요합니다. 이는 문제를 더 효율적으로 해결하고 관계를 강화하는 데 도움이 됩니다.'),(18,'모든 요청에 \'예\'라고 답하는 것은 나의 의지와 필요를 무시하게 만듭니다. 나의 한계를 알고 적절히 거절하는 것이 중요합니다. 이는 나의 자존감을 지키고 대인관계를 건강하게 유지하는 데 도움이 됩니다.'),(19,'올바르게 거절하는 것은 관계를 망치지 않습니다. 오히려, 솔직한 대화는 관계를 더욱 깊게 만들 수 있습니다. 서로의 한계를 존중하는 것이 중요합니다.'),(20,'거절할 줄 아는 것은 자신감의 표현입니다. 자신의 한계를 알고 그것을 표현하는 것이 진정한 용기입니다. 이는 타인에게 나의 경계를 명확히 알려주는 데 도움이 됩니다.'),(21,'거절하는 것은 연습을 통해 더욱 자연스러워질 수 있습니다. 작은 일에서부터 거절을 연습해보면, 점점 더 큰 일에서도 자연스럽게 거절할 수 있습니다. 이는 나의 의사결정 능력을 강화합니다.'),(22,'정당한 이유로 거절했을 때 미안해하지 말자. 나의 한계를 지키는 것은 당연한 일입니다. 과도한 죄책감은 나를 힘들게 할 뿐입니다. 거절은 내가 나 자신을 존중하는 한 방법입니다.'),(23,'거절할 때, 가능한 대안을 제시하면 상대방도 거절을 더 쉽게 받아들일 수 있습니다. 이는 상대방에게 존중받고 있다는 느낌을 주고 관계를 긍정적으로 유지하는 데 도움이 됩니다.'),(24,'자신의 감정과 필요를 우선시하는 것은 건강한 자아존중감을 형성하는 데 중요합니다. 다른 사람의 기대에 맞추기 위해 자신을 희생하는 것은 장기적으로 건강하지 않습니다.'),(25,'대부분의 사람들은 거절에 대해 이해할 수 있습니다. 너무 걱정하지 말고 솔직하게 말하는 것이 좋습니다. 이는 오해를 줄이고 관계를 긍정적으로 유지하는 데 도움이 됩니다.'),(26,'거절은 나의 기준과 경계를 명확히 하는 방법입니다. 나의 가치와 원칙을 지키기 위해 거절하는 것이 필요합니다. 이는 타인에게 나의 경계를 알리는 데 중요합니다.'),(27,'친구와의 관계에서 서로의 입장을 이해하려고 노력하면 갈등을 줄이고 더 깊은 유대감을 형성할 수 있습니다. 이는 상대방의 감정을 존중하고, 공감하는 능력을 키우는 데 도움이 됩니다.'),(28,'감정을 솔직하게 표현하면 상대방이 나의 상황과 감정을 더 잘 이해할 수 있습니다. 이는 오해를 줄이고, 신뢰를 쌓으며, 건강한 의사소통을 가능하게 합니다.'),(29,'서로 다른 관점을 존중하면 더 넓은 시각을 가지게 됩니다. 이는 서로의 차이를 이해하고, 갈등을 줄이며, 풍부한 대화를 나누는 데 도움이 됩니다.'),(30,'긍정적인 피드백은 상대방의 자존감을 높이고, 더 나은 행동을 유도하는 데 효과적입니다. 이는 건강한 대인관계를 유지하고, 서로의 성장을 지원하는 데 중요합니다.'),(31,'억지로 하는 배려는 나와 상대방 모두에게 부담이 됩니다. 자연스럽게 나오는 배려가 진정한 배려이며, 이는 서로를 더 편안하게 하고 관계를 긍정적으로 유지하는 데 도움이 됩니다.'),(32,'타산적인 배려는 상대방을 조작하려는 의도가 담겨 있어 진정한 배려가 아닙니다. 이는 오히려 신뢰를 손상시킬 수 있습니다. 순수한 마음에서 우러나오는 배려가 중요합니다.'),(33,'사람마다 생각과 느낌이 다르다는 사실을 인정하면 상대방을 더 잘 이해할 수 있습니다. 이는 상대방의 감정을 존중하고, 불필요한 갈등을 피하는 데 도움이 됩니다.'),(34,'상대방의 상황을 충분히 이해하지 못한 상태에서 결론을 내리는 것은 잘못된 판단으로 이어질 수 있습니다. 이는 오해를 줄이고, 상대방을 더 잘 이해하려는 노력을 통해 건강한 관계를 유지하는 데 중요합니다.'),(35,'조언은 때로는 상대방을 바꾸려는 시도로 받아들여질 수 있습니다. 반면, 공감은 상대방의 감정을 이해하고 존중하는 데 초점을 맞춥니다. 이는 서로의 감정을 더 깊이 이해하고 신뢰를 쌓는 데 도움이 됩니다.'),(36,'상호 존중이 없는 관계는 나에게 해로울 뿐입니다. 존중과 이해가 기반이 되는 관계만을 유지하는 것이 중요합니다.');

INSERT INTO character_data (character_id, ai_name, description, difficulty_level) VALUES
(1,'미연','미연은 매우 감성적인 타입이에요.\n부탁이 거절되면 실망하거나 슬퍼할 수 있어요. 미연은 내성적이지만 친구들에게는 따뜻하고 배려심이 많아 깊은 관계를 맺고 있으며, 친구들의 고민을 잘 들어줘요. 미연의 부탁을 공감하고 이해하며 부드럽게 거절하는 것이 중요해요.',1),(2,'세진','세진은 논리적이고 책임감이 강해 사람들과 쉽게 친해집니다. 하지만 세진은 매우 계산적이고 타산적인 성격을 가지고 있습니다. 어떤 일을 할 때 항상 이득과 손해를 따지며, 자신이 과거에 도와줬던 일에 대해서는 반드시 상대방이 갚아야 한다고 생각합니다. 세진은 이성적이고 차분하게 문제를 해결하려고 노력하며, 감정에 휘둘리지 않습니다. 이러한 성격 때문에 때로는 차갑게 보일 수 있지만, 그만큼 세진은 믿을 수 있는 사람입니다. 주변 사람들은 세진의 실용적이고 합리적인 면모를 존중하지만, 때로는 거리감을 느끼기도 합니다. 세진은 자신의 원칙을 굽히지 않으며, 필요할 때는 단호하게 대처합니다.',2),(3,'현아','현아는 포기하지 않고 끈기 있게 부탁을 반복하며, 솔직한 감정 표현으로 상대방의 동정을 얻으려 해요. 꾸준한 노력과 집요함으로 목표를 달성하지만, 때때로 그 성격이 상대방에게 부담이 될 수 있답니다.',3),(4,'진혁','진혁은 감정을 격하게 표현하는 성격으로, 분노 조절에 어려움을 겪습니다. 그는 매우 단순한 사고 방식을 가지고 있으며, 복잡한 상황이나 논리적 사고를 피합니다. 이러한 단순함은 그의 의사소통 방식에서도 드러나며, 주로 무례하거나 공격적인 부탁을 하는 경향이 있습니다.',4);


SET FOREIGN_KEY_CHECKS=1;
