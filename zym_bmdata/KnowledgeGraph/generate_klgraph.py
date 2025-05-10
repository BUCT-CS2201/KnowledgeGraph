import mysql.connector
from neo4j import GraphDatabase

class DataImporter:
    def __init__(self, mysql_config, neo4j_uri, neo4j_user, neo4j_password):
        # Connect to MySQL database
        self.mysql_connection = mysql.connector.connect(**mysql_config)
        self.neo4j_driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))

    def close(self):
        self.mysql_connection.close()
        self.neo4j_driver.close()

    def fetch_data(self, query):
        """Fetch data from MySQL"""
        cursor = self.mysql_connection.cursor(dictionary=True)
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        return rows

    def create_relic(self, relic):
        # 处理可能为 None 的字段
        relic_data = {k: (v if v is not None else "") for k, v in relic.items()}
        
        query = """
        MERGE (r:CulturalRelic {
            relic_id: $relic_id
        })
        SET r.name = $name,
            r.type = $type, 
            r.description = $description,
            r.size = $size,
            r.matrials = $matrials,
            r.dynasty = $dynasty,
            r.author = $author
        """
        with self.neo4j_driver.session() as session:
            session.run(query, **relic_data)

    def create_material(self, mat_name):
        if mat_name is None:
            return
        query = "MERGE (m:Material {material_name: $mat_name})"
        with self.neo4j_driver.session() as session:
            session.run(query, mat_name=mat_name)

    def create_dynasty(self, dynasty_name):
        if dynasty_name is None:
            return
        query = "MERGE (d:Dynasty {dynasty_name: $dynasty_name})"
        with self.neo4j_driver.session() as session:
            session.run(query, dynasty_name=dynasty_name)

    def create_museum(self, museum):
        # 处理可能为 None 的字段
        museum_data = {k: (v if v is not None else "") for k, v in museum.items()}
        
        query = """
        MERGE (m:Museum {
            museum_id: $museum_id
        })
        SET m.museum_name = $museum_name,
            m.description = $description,
            m.website_url = $website_url,
            m.booking_url = $booking_url
        """
        with self.neo4j_driver.session() as session:
            session.run(query, **museum_data)

    def create_address(self, addr):
        if not addr:  # 检查地址是否为空
            return
        query = "MERGE (a:Address {address_text: $addr})"
        with self.neo4j_driver.session() as session:
            session.run(query, addr=addr)

    def create_relic_image(self, img):
        # 处理可能为空的情况
        image_id = img.get('image_id')
        img_url = img.get('img_url', "")
        
        if not image_id:
            return
            
        query = """
        MERGE (i:RelicImage {
            image_id: $image_id
        })
        SET i.img_url = $img_url
        """
        with self.neo4j_driver.session() as session:
            session.run(query, image_id=image_id, img_url=img_url)

    def create_museum_image(self, img):
        # 处理可能为空的情况
        image_id = img.get('image_id')
        img_url = img.get('img_url', "")
        
        if not image_id:
            return
            
        query = """
        MERGE (i:MuseumImage {
            image_id: $image_id
        })
        SET i.img_url = $img_url
        """
        with self.neo4j_driver.session() as session:
            session.run(query, image_id=image_id, img_url=img_url)

    def create_relationship_relic_material(self, relic_id, mat_name):
        if not mat_name:
            return
        query = """
        MATCH (r:CulturalRelic {relic_id: $relic_id})
        MATCH (m:Material {material_name: $mat_name})
        MERGE (r)-[:MADE_OF]->(m)
        """
        with self.neo4j_driver.session() as session:
            session.run(query, relic_id=relic_id, mat_name=mat_name)

    def create_relationship_relic_dynasty(self, relic_id, dynasty):
        if not dynasty:
            return
        query = """
        MATCH (r:CulturalRelic {relic_id: $relic_id})
        MATCH (d:Dynasty {dynasty_name: $dynasty})
        MERGE (r)-[:FROM_DYNASTY]->(d)
        """
        with self.neo4j_driver.session() as session:
            session.run(query, relic_id=relic_id, dynasty=dynasty)

    def create_relationship_relic_museum(self, relic_id, museum_id):
        if not relic_id or not museum_id:
            return
        query = """
        MATCH (r:CulturalRelic {relic_id: $relic_id})
        MATCH (m:Museum {museum_id: $museum_id})
        MERGE (r)-[:IN_MUSEUM]->(m)
        """
        with self.neo4j_driver.session() as session:
            session.run(query, relic_id=relic_id, museum_id=museum_id)

    def create_relationship_museum_address(self, museum_id, address):
        if not museum_id or not address:
            return
        try:
            # 首先确保地址节点存在
            address_query = "MERGE (a:Address {address_text: $address})"
            with self.neo4j_driver.session() as session:
                session.run(address_query, address=address)
            
            # 然后创建关系
            query = """
            MATCH (m:Museum {museum_id: $museum_id})
            MATCH (a:Address {address_text: $address})
            MERGE (m)-[:HAS_ADDRESS]->(a)
            """
            with self.neo4j_driver.session() as session:
                result = session.run(query, museum_id=museum_id, address=address)
                summary = result.consume()
                if summary.counters.relationships_created > 0:
                    print(f"成功创建博物馆 {museum_id} 与地址 '{address}' 的关系")
                else:
                    print(f"警告: 博物馆 {museum_id} 与地址 '{address}' 的关系可能未创建")
        except Exception as e:
            print(f"创建博物馆 {museum_id} 与地址 '{address}' 的关系失败: {str(e)}")

    def create_relationship_relic_image(self, relic_id, image_id):
        if not relic_id or not image_id:
            return
        try:
            query = """
            MATCH (r:CulturalRelic {relic_id: $relic_id})
            MATCH (i:RelicImage {image_id: $image_id})
            MERGE (r)-[:HAS_IMAGE]->(i)
            """
            with self.neo4j_driver.session() as session:
                session.run(query, relic_id=relic_id, image_id=image_id)
            print(f"成功创建文物 {relic_id} 与图片 {image_id} 的关系")
        except Exception as e:
            print(f"创建文物 {relic_id} 与图片 {image_id} 的关系失败: {str(e)}")

    def create_relationship_museum_image(self, museum_id, image_id):
        if not museum_id or not image_id:
            return
        
        try:
            query = """
            MATCH (m:Museum {museum_id: $museum_id})
            MATCH (i:MuseumImage {image_id: $image_id})
            MERGE (m)-[:HAS_IMAGE]->(i)
            """
            with self.neo4j_driver.session() as session:
                session.run(query, museum_id=museum_id, image_id=image_id)
            print(f"成功创建博物馆 {museum_id} 与图片 {image_id} 的关系")
        except Exception as e:
            print(f"创建博物馆 {museum_id} 与图片 {image_id} 的关系失败: {str(e)}")


    def import_data(self):
        # 1) 取出 relic 和其它简单表
        relics        = self.fetch_data("SELECT * FROM cultural_relic")
        materials     = self.fetch_data("SELECT DISTINCT matrials FROM cultural_relic")
        dynasties     = self.fetch_data("SELECT DISTINCT dynasty FROM cultural_relic")
        museums       = self.fetch_data("SELECT * FROM museum")  # 获取所有博物馆信息，包括地址
        
        # 检查博物馆地址数据
        print(f"获取到 {len(museums)} 个博物馆记录")
        addresses_count = sum(1 for mu in museums if mu.get('address'))
        print(f"其中 {addresses_count} 个博物馆有地址信息")
        
        # 将 museum_id 和 address 映射为字典，确保地址不为 None 或空字符串
        addresses = {}
        for mu in museums:
            if mu.get('address') and mu.get('address').strip():
                addresses[mu['museum_id']] = mu['address'].strip()
                
        print(f"有效地址映射数量: {len(addresses)}")

        # 获取所有图片数据
        relic_images  = self.fetch_data("SELECT * FROM relic_image")
        museum_images = self.fetch_data("SELECT * FROM museum_image")

        # 为每个遗物和博物馆预先映射图片 ID
        relic_image_map = {}
        for img in relic_images:
            relic_id = img['relic_id']
            if relic_id not in relic_image_map:
                relic_image_map[relic_id] = []
            relic_image_map[relic_id].append(img['image_id'])

        museum_image_map = {}
        for img in museum_images:
            museum_id = img['museum_id']
            if museum_id not in museum_image_map:
                museum_image_map[museum_id] = []
            museum_image_map[museum_id].append(img['image_id'])

        # 创建材料节点
        print("创建材料节点...")
        for m in materials:
            if m['matrials']:  # 确保材料不为空
                self.create_material(m['matrials'])

        # 创建朝代节点
        print("创建朝代节点...")
        for d in dynasties:
            if d['dynasty']:  # 确保朝代不为空
                self.create_dynasty(d['dynasty'])

        # 创建博物馆节点
        print("创建博物馆节点...")
        for mu in museums:
            self.create_museum(mu)

        # 创建地址节点
        print("创建地址节点...")
        for museum_id, addr in addresses.items():
            if addr:  # 确保地址不为空
                self.create_address(addr)
                print(f"为博物馆 {museum_id} 创建地址节点: '{addr}'")

        # 创建文物图片节点
        print("创建文物图片节点...")
        for img in relic_images:
            self.create_relic_image(img)

        # 创建博物馆图片节点
        print("创建博物馆图片节点...")
        for img in museum_images:
            self.create_museum_image(img)

        # 创建遗物节点
        print("创建遗物节点...")
        for r in relics:
            self.create_relic(r)

        # 创建关系
        print("创建关系...")
        for r in relics:
            relic_id = r['relic_id']
            
            # 遗物与材料的关系
            self.create_relationship_relic_material(relic_id, r['matrials'])
            
            # 遗物与朝代的关系
            self.create_relationship_relic_dynasty(relic_id, r['dynasty'])
            
            # 遗物与博物馆的关系
            museum_id = r['museum_id']
            self.create_relationship_relic_museum(relic_id, museum_id)
            
            # 博物馆与地址的关系不在这里处理
            
            # 遗物与图片的关系
            relic_image_ids = relic_image_map.get(relic_id, [])
            for image_id in relic_image_ids:
                self.create_relationship_relic_image(relic_id, image_id)
        
        # 创建博物馆与图片的关系（作为单独循环处理以确保不遗漏）
        print("创建博物馆与图片的关系...")
        for museum_id, image_ids in museum_image_map.items():
            for image_id in image_ids:
                self.create_relationship_museum_image(museum_id, image_id)
        
        # 单独处理博物馆与地址的关系
        print("创建博物馆与地址的关系...")
        museum_address_count = 0
        for museum_id, address in addresses.items():
            self.create_relationship_museum_address(museum_id, address)
            museum_address_count += 1
        
        print(f"总共尝试创建 {museum_address_count} 个博物馆-地址关系")
        print("导入完成")

# 配置并运行
mysql_config = {
    'user':     'root',
    'password': 'jike2201!',
    'host':     '123.56.47.51',
    'port':     3308,
    'database': 'cultural_relics'
}
neo4j_uri      = "bolt://123.56.47.51:7687"
neo4j_user     = "neo4j"
neo4j_password = "jike2201!"

if __name__ == '__main__':
    importer = DataImporter(mysql_config, neo4j_uri, neo4j_user, neo4j_password)
    importer.import_data()
    importer.close()
    print("程序执行完毕")
