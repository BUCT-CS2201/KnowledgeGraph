# KnowledgeGraph
知识图谱子系统
## 下载朱一鸣的爬取代码自带数据清洗，可以爬取每个商品独有的信息，只是速度较慢因此做数据清洗的同学需要商量每人爬取不同的页面进行整理

## 下载朱一鸣的知识图谱构建代码，该代码构建关系如下：
### MADE_OF：文物与材料之间的关系
连接方向：文物 (CulturalRelic) → 材料 (Material)
表示：文物由某种材料制成
### FROM_DYNASTY：文物与朝代之间的关系
连接方向：文物 (CulturalRelic) → 朝代 (Dynasty)
表示：文物来源于特定的历史朝代
### IN_MUSEUM：文物与博物馆之间的关系
连接方向：文物 (CulturalRelic) → 博物馆 (Museum)
表示：文物收藏于特定博物馆
### HAS_ADDRESS：博物馆与地址之间的关系
连接方向：博物馆 (Museum) → 地址 (Address)
表示：博物馆位于特定的地理位置
### HAS_IMAGE：两种不同类型的图片关系
文物图片关系：文物 (CulturalRelic) → 图片 (RelicImage)
博物馆图片关系：博物馆 (Museum) → 图片 (MuseumImage)
表示：实体拥有相关的图像资料
### 附加说明
加入新数据前要删除旧数据运行在neo4j中运行以下指令
// 删除 CulturalRelic 和相关关系
MATCH (n:CulturalRelic)-[r]->()
DELETE r, n;

// 删除 Material 和相关关系
MATCH (n:Material)-[r]->()
DELETE r, n;

// 删除 Museum 和相关关系
MATCH (n:Museum)-[r]->()
DELETE r, n;

// 删除 RelicImage 和相关关系
MATCH (n:RelicImage)-[r]->()
DELETE r, n;

// 删除 MuseumImage 和相关关系
MATCH (n:MuseumImage)-[r]->()
DELETE r, n;

// 删除 Address 和相关关系
MATCH (n:Address)-[r]->()
DELETE r, n;

// 删除 Dynasty 和相关关系
MATCH (n:Dynasty)-[r]->()
DELETE r, n;

MATCH (n:CulturalRelic)
WHERE NOT (n)--()
DELETE n;

MATCH (n:Material)
WHERE NOT (n)--()
DELETE n;

MATCH (n:Museum)
WHERE NOT (n)--()
DELETE n;

MATCH (n:RelicImage)
WHERE NOT (n)--()
DELETE n;

MATCH (n:MuseumImage)
WHERE NOT (n)--()
DELETE n;

MATCH (n:Address)
WHERE NOT (n)--()
DELETE n;

MATCH (n:Dynasty)
WHERE NOT (n)--()
DELETE n;
