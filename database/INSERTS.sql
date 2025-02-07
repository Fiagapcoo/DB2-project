-- Inserção de usuários na tabela HR.Users
INSERT INTO HR.Users (Name, Phone, Email, HashedPassword, ProfilePic, IsManager)
VALUES 
('João Silva', '+351912345678', 'joao.silva@email.com', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', TRUE),
('Maria Oliveira', '+351923456789', 'maria.oliveira@email.com', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', FALSE),
('Pedro Santos', '+351934567890', 'pedro.santos@email.com', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', FALSE);

-- Inserção de endereços na tabela HR.User_address
INSERT INTO HR.User_address (UserID, Address_line1, Address_line2, City, Postal_code, Country, Phone_number)
VALUES 
(1, 'Rua das Flores, 123', NULL, 'Lisboa', '1000-001', 'Portugal', '+351912345678'),
(2, 'Avenida da Liberdade, 456', 'Apt. 12', 'Porto', '4000-002', 'Portugal', '+351923456789'),
(3, 'Rua do Comércio, 789', NULL, 'Coimbra', '3000-003', 'Portugal', '+351934567890');

-- Inserção de métodos de pagamento na tabela HR.User_payment
INSERT INTO HR.User_payment (UserID, Payment_method, Provider, CardNumber, ExpiryDate, Billing_AddressID)
VALUES 
(1, 'Credit Card', 'Visa', '4111111111111111', '2026-05-01', 1),
(2, 'PayPal', 'PayPal', 'maria.oliveira@email.com', NULL, 2),
(3, 'Debit Card', 'Mastercard', '5500000000000004', '2027-07-01', 3);

-- Inserção de categorias na tabela STATIC_CONTENT.Categories
INSERT INTO STATIC_CONTENT.Categories (Name, Description, preview_img)
VALUES 
('Bateria e Percussão', 'Baterias, tambores e percussão em geral', 'https://thumbs.static-thomann.de/thumb/thumb150x150/pics/images/category/icons/main/dr.webp'),
('Microfones', 'Microfones de estúdio e ao vivo', 'https://thumbs.static-thomann.de/thumb/thumb150x150/pics/images/category/icons/main/mi.webp'),
('Guitarras e Baixo', 'Guitarras elétricas, acústicas e baixos', 'https://thumbs.static-thomann.de/thumb/thumb150x150/pics/images/category/icons/main/gi.webp'),
('Teclados', 'Teclados e pianos digitais', 'https://thumbs.static-thomann.de/thumb/thumb150x150/pics/images/category/icons/main/ta.webp'),
('Equipamentos PA', 'Caixas de som, amplificadores e mixers', 'https://thumbs.static-thomann.de/thumb/thumb150x150/pics/images/category/icons/main/pa.webp'),
('Acessórios', 'Cabos, palhetas e outros acessórios', 'https://thumbs.static-thomann.de/thumb/thumb150x150/pics/images/category/icons/main/zu.webp');


-- Inserção de marcas na tabela DYNAMIC_CONTENT.brands
INSERT INTO DYNAMIC_CONTENT.brands (brandname)
VALUES
('Pearl'),
('Roland'),
('Mapex'),
('Tama'),
('Ludwig'),
('DW (Drum Workshop)'),
('Yamaha'),
('Zildjian'),
('Vic Firth'),
('Shure'),
('Audio-Technica'),
('Sennheiser'),
('Neumann'),
('Rode'),
('AKG'),
('Electro-Voice'),
('Beyerdynamic'),
('Harley Benton'),
('Gibson'),
('Ibanez'),
('PRS (Paul Reed Smith)'),
('Fender'),
('Music Man'),
('Epiphone'),
('Cort'),
('Squier'),
('Casio'),
('Korg'),
('Nord'),
('Kurzweil'),
('Arturia'),
('Behringer'),
('PRO Snake');

-- Inserção de produtos na tabela DYNAMIC_CONTENT.Products
INSERT INTO DYNAMIC_CONTENT.Products (Name, Description, BasePrice, DiscountedPrice, SKU, ModelID, ProductSerialNumber, CategoryID, producttype, image_url, BrandID)
VALUES
('Pearl Export Series', 'Bateria acústica completa com ferragens', 1300.00, 1250.00, 'DRUM-002', NULL, 'SN111111', 1, 'instrument', 'https://thumbs.static-thomann.de/thumb/bdbmagic/pics/bdb/_31/313175/11844135_800.jpg', 1),
('Roland TD-17KVX', 'Bateria eletrônica com pads de mesh', 1800.00, 1700.00, 'DRUM-003', NULL, 'SN222222', 1, 'instrument', 'https://thumbs.static-thomann.de/thumb/bdbmagic/pics/bdb/_55/551837/17954422_800.jpg', 2),
('Mapex Mars Birch', 'Bateria acústica com tons equilibrados', 1200.00, NULL, 'DRUM-004', NULL, 'SN333333', 1, 'instrument', 'https://thumbs.static-thomann.de/thumb/bdbmagic/pics/bdb/_56/564235/18952743_800.jpg', 3),
('Tama Imperialstar', 'Kit completo com ferragens e pratos', 1400.00, 1350.00, 'DRUM-005', NULL, 'SN444444', 1, 'instrument', 'https://thumbs.static-thomann.de/thumb/bdbmagic/pics/bdb/_57/575866/18838043_800.jpg', 4),
('Ludwig Breakbeats', 'Bateria compacta para shows ao vivo', 900.00, 850.00, 'DRUM-006', NULL, 'SN555555', 1, 'instrument', 'https://thumbs.static-thomann.de/thumb/bdbmagic/pics/bdb/_57/578810/18691932_800.jpg', 5),
('DW Performance Series', 'Bateria premium para profissionais', 2500.00, NULL, 'DRUM-007', NULL, 'SN666666', 1, 'instrument', 'https://thumbs.static-thomann.de/thumb/bdbmagic/pics/bdb/_53/535079/17072123_800.jpg', 6),
('Yamaha DTX6K-X', 'Bateria eletrônica de alta qualidade', 1900.00, 1800.00, 'DRUM-008', NULL, 'SN777777', 1, 'instrument', 'https://thumbs.static-thomann.de/thumb/bdbmagic/pics/bdb/_50/507768/15948865_800.jpg', 7),
('Zildjian A Custom', 'Pratos profissionais brilhantes', 1100.00, NULL, 'DRUM-010', NULL, 'SN999999', 1, 'instrument', 'https://thumbs.static-thomann.de/thumb/bdbmagic/pics/bdb/_10/100718/10751194_800.jpg', 8),
('Vic Firth 5A', 'Baquetas de madeira clássicas', 15.00, NULL, 'DRUM-011', NULL, 'SN101010', 1, 'instrument', 'https://thumbs.static-thomann.de/thumb/bdbmagic/pics/bdb/_10/101808/13307896_800.jpg', 9),
('Shure SM57', 'Microfone dinâmico para instrumentos', 130.00, 120.00, 'MIC-002', NULL, 'SN202020', 2, 'instrument', 'https://fast-images.static-thomann.de/pics/bdb/_24/247992/12657636_800.jpg', 10),
('Audio-Technica AT2020', 'Microfone condensador para estúdio', 150.00, NULL, 'MIC-003', NULL, 'SN303030', 2, 'instrument', 'https://fast-images.static-thomann.de/pics/bdb/_20/208026/12645601_800.jpg', 11),
('Sennheiser e835', 'Microfone dinâmico cardioide para palco', 120.00, NULL, 'MIC-004', NULL, 'SN404040', 2, 'instrument', 'https://fast-images.static-thomann.de/pics/bdb/_50/506353/15672705_800.jpg', 12),
('Neumann TLM 103', 'Microfone condensador profissional de estúdio', 1100.00, 1050.00, 'MIC-005', NULL, 'SN505050', 2, 'instrument', 'https://thumbs.static-thomann.de/thumb/bdbmagic/pics/bdb/_17/174067/6985971_800.jpg', 13),
('Rode NT1-A', 'Microfone condensador de alta sensibilidade', 230.00, NULL, 'MIC-006', NULL, 'SN606060', 2, 'instrument', 'https://fast-images.static-thomann.de/pics/bdb/_25/251204/12563646_800.jpg', 14),
('AKG P120', 'Microfone condensador para gravações', 100.00, 90.00, 'MIC-007', NULL, 'SN707070', 2, 'instrument', 'https://thumbs.static-thomann.de/thumb/bdbmagic/pics/bdb/_34/345414/8998179_800.jpg', 15),
('Electro-Voice RE20', 'Microfone de broadcast para rádio e podcasts', 500.00, NULL, 'MIC-008', NULL, 'SN808080', 2, 'instrument', 'https://thumbs.static-thomann.de/thumb/bdbmagic/pics/bdb/_12/128926/10589653_800.jpg', 16),
('Beyerdynamic M88TG', 'Microfone dinâmico para palco e instrumentos', 350.00, NULL, 'MIC-009', NULL, 'SN909090', 2, 'instrument', 'https://thumbs.static-thomann.de/thumb/bdbmagic/pics/bdb/_57/573620/18552223_800.jpg', 17),
('Shure SM7B', 'Microfone dinâmico para voz e podcast', 400.00, 380.00, 'MIC-010', NULL, 'SN010101', 2, 'instrument', 'https://thumbs.static-thomann.de/thumb/bdbmagic/pics/bdb/_12/129929/18086262_800.jpg', 10),
('Sennheiser MD 421-II', 'Microfone dinâmico versátil para palco e estúdio', 380.00, NULL, 'MIC-011', NULL, 'SN111111', 2, 'instrument', 'https://thumbs.static-thomann.de/thumb/bdbmagic/pics/bdb/_59/598567/19393903_800.jpg', 12),
('Harley Benton TE-52', 'Guitarra elétrica clássica', 950.00, 900.00, 'GUIT-002', NULL, 'SN121212', 3, 'instrument', 'https://fast-images.static-thomann.de/pics/bdb/_22/223985/19675769_800.jpg', 18),
('Gibson Les Paul Standard', 'Modelo icônico com som encorpado', 2500.00, 2400.00, 'GUIT-003', NULL, 'SN131313', 3, 'instrument', 'https://fast-images.static-thomann.de/pics/bdb/_46/462510/14952105_800.jpg', 19),
('Ibanez RG550', 'Guitarra veloz para rock e metal', 1200.00, 1150.00, 'GUIT-004', NULL, 'SN141414', 3, 'instrument', 'https://thumbs.static-thomann.de/thumb/bdbmagic/pics/bdb/_59/597464/19350266_800.jpg', 20),
('PRS Custom 24', 'Guitarra de alta qualidade', 2300.00, NULL, 'GUIT-005', NULL, 'SN151515', 3, 'instrument', 'https://fast-images.static-thomann.de/pics/bdb/_56/569034/18480653_800.jpg', 21),
('Yamaha Pacifica 112V', 'Ótima para iniciantes e intermediários', 350.00, 330.00, 'GUIT-006', NULL, 'SN161616', 3, 'instrument', 'https://fast-images.static-thomann.de/pics/bdb/_51/514386/16044123_800.jpg', 7),
('Fender Precision Bass', 'Baixo elétrico clássico e poderoso', 1400.00, 1300.00, 'GUIT-007', NULL, 'SN171717', 3, 'instrument', 'https://fast-images.static-thomann.de/pics/bdb/_44/449512/14622783_800.jpg', 22),
('Music Man StingRay', 'Baixo profissional de 4 cordas', 2200.00, NULL, 'GUIT-008', NULL, 'SN181818', 3, 'instrument', 'https://thumbs.static-thomann.de/thumb/bdbmagic/pics/bdb/_57/577429/18615988_800.jpg', 23),
('Epiphone SG Standard', 'Guitarra acessível e potente', 600.00, 550.00, 'GUIT-009', NULL, 'SN191919', 3, 'instrument', 'https://fast-images.static-thomann.de/pics/bdb/_48/482569/15170413_800.jpg', 24),
('Cort Action Bass', 'Baixo acessível para iniciantes', 300.00, 280.00, 'GUIT-010', NULL, 'SN202020', 3, 'instrument', 'https://thumbs.static-thomann.de/thumb/bdbmagic/pics/bdb/_58/587848/19005285_800.jpg', 25),
('Squier Classic Vibe 50s', 'Guitarra com visual vintage', 450.00, 430.00, 'GUIT-011', NULL, 'SN212121', 3, 'instrument', 'https://fast-images.static-thomann.de/pics/bdb/_46/468405/14991815_800.jpg', 26),
('Yamaha P-525', 'Piano digital de 88 teclas', 700.00, 650.00, 'KEY-002', NULL, 'SN313131', 4, 'instrument', 'https://thumbs.static-thomann.de/thumb/bdbmagic/pics/bdb/_57/579591/18717642_800.jpg', 7),
('Roland FP-30X', 'Piano digital portátil', 800.00, NULL, 'KEY-003', NULL, 'SN323232', 4, 'instrument', 'https://fast-images.static-thomann.de/pics/bdb/_42/429218/12747602_800.jpg', 2),
('Casio PX-S1100', 'Piano digital slim e elegante', 600.00, 580.00, 'KEY-004', NULL, 'SN333333', 4, 'instrument', 'https://thumbs.static-thomann.de/thumb/bdbmagic/pics/bdb/_52/528199/16768724_800.jpg', 27),
('Korg Kronos 88', 'Workstation para estúdio e palco', 3500.00, NULL, 'KEY-005', NULL, 'SN343434', 4, 'instrument', 'https://thumbs.static-thomann.de/thumb/bdbmagic/pics/bdb/_60/609236/19777774_800.jpg', 28),
('Nord Stage 3', 'Teclado profissional para shows', 4000.00, 3900.00, 'KEY-006', NULL, 'SN353535', 4, 'instrument', 'https://thumbs.static-thomann.de/thumb/bdbmagic/pics/bdb/_56/560977/18566068_800.jpg', 29),
('Casio CT-S500', 'Teclado para iniciantes e estudantes', 300.00, 280.00, 'KEY-007', NULL, 'SN363636', 4, 'instrument', 'https://fast-images.static-thomann.de/pics/bdb/_53/537364/17381076_800.jpg', 27),
('Korg Kross 2', 'Workstation acessível', 900.00, NULL, 'KEY-008', NULL, 'SN373737', 4, 'instrument', 'https://thumbs.static-thomann.de/thumb/bdbmagic/pics/bdb/_42/421619/12592841_800.jpg', 28),
('Kurzweil K2700', 'Piano digital com som de alta qualidade', 1200.00, NULL, 'KEY-009', NULL, 'SN383838', 4, 'instrument', 'https://thumbs.static-thomann.de/thumb/bdbmagic/pics/bdb/_51/519922/17137748_800.jpg', 30),
('Roland RD-2000', 'Piano de palco profissional', 2500.00, 2400.00, 'KEY-010', NULL, 'SN393939', 4, 'instrument', 'https://thumbs.static-thomann.de/thumb/bdbmagic/pics/bdb/_59/596971/19450221_800.jpg', 2),
('Arturia KeyLab 49', 'Teclado controlador MIDI', 450.00, NULL, 'KEY-011', NULL, 'SN404040', 4, 'instrument', 'https://thumbs.static-thomann.de/thumb/bdbmagic/pics/bdb/_56/567139/18249455_800.jpg', 31),
('Behringer X32', 'Mesa de som digital para grandes eventos', 2500.00, 2400.00, 'PA-001', NULL, 'SN678901', 5, 'instrument', 'https://fast-images.static-thomann.de/pics/bdb/_31/319068/16714704_800.jpg', 32),
('Cabo PRO Snake TPM 10', 'Cabo para microfone de alta qualidade', 20.00, 18.00, 'ACC-001', NULL, 'SN123987', 6, 'accessories', 'https://thumbs.static-thomann.de/thumb/bdbmagic/pics/bdb/_21/213367/19117933_800.jpg', 33);

-- Inserção de estoque na tabela DYNAMIC_CONTENT.Stock
INSERT INTO DYNAMIC_CONTENT.Stock (ProductID, Quantity)
VALUES 
(1, 0),
(2, 96),
(3, 55),
(4, 44),
(5, 59),
(6, 81),
(7, 62),
(8, 86),
(9, 76),
(10, 0),
(11, 50),
(12, 19),
(13, 88),
(14, 37),
(15, 62),
(16, 55),
(17, 91),
(18, 62),
(19, 14),
(20, 0),
(21, 61),
(22, 68),
(23, 64),
(24, 18),
(25, 75),
(26, 65),
(27, 87),
(28, 88),
(29, 70),
(30, 34),
(31, 88),
(32, 0),
(33, 48),
(34, 30),
(35, 52),
(36, 51),
(37, 16),
(38, 97),
(39, 93),
(40, 46),
(41, 67);

-- Inserção de pedidos na tabela TRANSACTIONS.Orders
INSERT INTO TRANSACTIONS.Orders (UserID, TransactionCode, Status, CartContentJSON)
VALUES 
(1, 'TXN54321', 'Completed', '{"items": [{"product_id": 5, "quantity": 2}, {"product_id": 12, "quantity": 1}]}'),
(2, 'TXN98765', 'Pending', '{"items": [{"product_id": 8, "quantity": 1}, {"product_id": 14, "quantity": 1}]}');

-- Inserção de pagamentos na tabela TRANSACTIONS.Payments
INSERT INTO TRANSACTIONS.Payments (OrderID, UserID, PaymentMethod, PaymentStatus, Amount)
VALUES 
(1, 1, 'Credit Card', 'Paid', 1950.00),
(2, 2, 'PayPal', 'Pending', 260.00);


