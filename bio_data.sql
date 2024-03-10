INSERT INTO role (role_name) VALUES ('admin'), ('staff'), ('horticulturalist');

INSERT INTO position (position_name) VALUES ('Manager'), ('Assistant'), ('Supervisor'),('Coordinator'),('Intern') ;
INSERT INTO department (department_name) VALUES ('Administration'), ('Human Resources'), ('Operations'), ('Marketing'), ('Research and Development') ;

INSERT INTO user (username, hashed_password, salt, first_name, last_name, email,phone, join_date, role_id, status) VALUES
('testuser', '5fae31539e070a690c1b63720c25eb5b86084b5098a942c86c89c1d67157ed6b', 'abcd', 'John', 'Smith', 'johnsmith@example.com', '1234567890', '2023-01-01', 3, 1),
('janedoe', '5fae31539e070a690c1b63720c25eb5b86084b5098a942c86c89c1d67157ed6b', 'abcd', 'Jane', 'Doe', 'janedoe@example.com', '4567890123', '2023-01-01', 3, 1),
('testadmin', '5fae31539e070a690c1b63720c25eb5b86084b5098a942c86c89c1d67157ed6b', 'abcd', 'Michael', 'Brown', 'michaelbrown@example.com', '1234567890', '2023-01-01', 1,  1),
('emilywilson', '5fae31539e070a690c1b63720c25eb5b86084b5098a942c86c89c1d67157ed6b', 'abcd', 'Emily', 'Wilson','emilywilson@example.com','4567890123', '2023-02-15',  2,  1),
('sophiethompson', '5fae31539e070a690c1b63720c25eb5b86084b5098a942c86c89c1d67157ed6b', 'abcd', 'Sophie', 'Thompson','sophiethompson@example.com', '7890123456', '2023-03-15', 3, 1),
('davidjones',  '5fae31539e070a690c1b63720c25eb5b86084b5098a942c86c89c1d67157ed6b', 'abcd','David', 'Jones', 'davidjones@example.com','3216549870', '2023-04-01',3,  1),
('robertmartin','5fae31539e070a690c1b63720c25eb5b86084b5098a942c86c89c1d67157ed6b', 'abcd','Robert', 'Martin', 'robertmartin@example.com', '9876543210', '2023-05-01',  3, 1),
('jenniferclark',  '5fae31539e070a690c1b63720c25eb5b86084b5098a942c86c89c1d67157ed6b', 'abcd', 'Jennifer', 'Clark','jenniferclark@example.com', '7890123456', '2023-02-15',2,  1),
('teststaff',  '5fae31539e070a690c1b63720c25eb5b86084b5098a942c86c89c1d67157ed6b', 'abcd','Mary', 'Robinson', 'maryrobinson@example.com','3216549870', '2023-04-01', 2,  1);


INSERT INTO horticulturalist (user_id, horticulturalist_id, address) VALUES
(1, 'HORT2023010100001', '123 Garden St'),
(2, 'HORT2023010100002', '456 Green Ave'),
(5, 'HORT2023031500001', '789 Flower Rd'),
(6, 'HORT2023040100001', '321 Orchard Ln'),
(7, 'HORT2023050100001', '987 Park Blvd');

INSERT INTO staff (user_id, staff_id, hire_date, position_id, department_id) VALUES
(3, 'STAFF2023010100001', '2023-01-01', 1, 1),
(4, 'STAFF2023021500001', '2023-02-15', 2, 2),
(8, 'STAFF2023021500002', '2023-02-15', 3, 3),
(9, 'STAFF2023040100001', '2023-04-01', 4, 4);


INSERT INTO biosecurity (common_name, scientific_name, key_char, biology, impact, source_url, is_present_in_nz) VALUES
# Disease not in NZ
('Aster yellows phytoplasma', 'Candidatus Phytoplasma asteris', 
'The symptoms vary markedly depending on the host plant. And the symptoms aren''t unique to aster yellows phytoplasma.
Symptoms include:

abnormal growth, 
overall stunting,
stems with a ''witch''s broom'' appearance,
bunchy growth, yellow leaves, 
leaf-like structures instead of flowers (phyllody), 
unusual greening of flowers (virescence).',

'It has a large host range recorded, across many different plant families.  Hosts overseas include maize, roses, apples, brassicas (like broccoli), gladiolus, clover, citrus, onions, even the hydrangea.

Aster yellows phytoplasma can move into healthy plants by grafting from infected plants.  We know some leafhoppers can transfer the bacteria between plants when they feed.',

'Aster yellows phytoplasma causes abnormalities in plant growth. A reduction in the quality and quantity of plant yield would be the main problem if it established here.

Its likely impact in New Zealand would depend on:

which plants are affected
whether we have leafhoppers that can carry the bacteria.
At the moment, we don''t know whether the insects we have in New Zealand transmit the bacteria.',

'https://www.mpi.govt.nz/biosecurity/pests-and-diseases-not-in-new-zealand/horticultural-pests-and-diseases-not-in-nz/aster-yellows-phytoplasma/',
0),
#2
('Avocado sunblotch disease', 'Avocado sunblotch viroid', 
'Typical avocado sunblotch symptoms include:

stunted growth and fewer fruit,
yellow, red, or white discolorations on the skin,
sunken areas and lesions on fruit,
small or misshapen fruit,
red, pink, white, or yellow streaks on the tree bark or twigs,
deformed leaves with bleached-looking, yellow or white areas.',

'The sunblotch viroid comes from the same places avocados do – Central and South America. It only affects avocados.',

'Avocado sunblotch disease damages avocado trees and fruit, meaning fewer fruit are produced.

If the disease was found here, international trade in avocado fruit is likely to be affected.',

'https://www.mpi.govt.nz/biosecurity/pests-and-diseases-not-in-new-zealand/horticultural-pests-and-diseases-not-in-nz/avocado-sunblotch-disease/',
0),
#3
('Bacterial leaf scorch', 'Xylella fastidiosa', 
'Scorched leaves are a sign of some other plant diseases already present in New Zealand. Plants infected with Xylella show:

scorched leaves
browning
loss of leaves
stunted shoots
reduced fruit size
over time, dieback and death of the plant.',

'This bacterium can infect many host plants. It causes different diseases in different hosts. It affects plants important to New Zealand, like grapes, olives and citrus. The bacterium multiplies and blocks the water transport system in plants. It stops the water getting from the roots to the leaves.

It goes by many names, such as Pierce''s disease in grapes, olive quick decline syndrome, and citrus variegated chlorosis.

This bacterium has killed 1,000-year-old olive trees in Italy and initially devastated vineyards in California. Although, it''s now managed in California.',

'Xylella is one of the most important plant diseases that MPI wants to keep out of New Zealand. It is an invasive bacterial plant disease that is spreading around the world. We regularly find out about new host plants that Xylella can infect.

Overseas, Xylella has caused devastating diseases in crops like grapes, olives and citrus. These are important to New Zealand''s economy.

Scientists have found the bacterium in some of our native plants that were growing in California.',

'https://www.mpi.govt.nz/biosecurity/pests-and-diseases-not-in-new-zealand/horticultural-pests-and-diseases-not-in-nz/bacterial-leaf-scorch/',
0),
#4
('Bacterial soft rot', 'Pantoea ananatis', 
'The signs of a Pantoea ananatis infection can be similar to other diseases. Diagnosis requires an expert. The severity of these diseases can vary depending on conditions, like humidity and temperature.',

'These bacteria can cause disease in onions, eucalyptus, tomatoes, melons, maize, and other plants. There are different strains of the bacteria. Some can be helpful, some harmful, and some harmless. Scientists are still learning about the benefits and risks of the different strains of bacteria.',

'The bacteria have caused serious crop losses overseas. They can cause diseases such as:

stalk rot, bacterial wilt, and leaf blight in maize
bacterial leaf blight and shoot tip dieback in 2 types of eucalyptus
centre rot in onions
grey wall in tomatoes
internal rot in melons.',

'https://www.mpi.govt.nz/biosecurity/pests-and-diseases-not-in-new-zealand/horticultural-pests-and-diseases-not-in-nz/bacterial-soft-rot/',
0),
#5
('Black rot', 'Guignardia bidwellii', 
'You will see small brown circular spots on young grape leaves (older leaves can resist the rot). The symptoms on leaves can be confused with other fungi.

Black rot infects grapes when they''re still green. You will see light brown spots that become dark brown. Eventually, the spots cover the whole fruit.',

'This is a fungus that causes diseases on grapes and some ornamental plants. It''s native to North America and parts of Europe.',

'This fungus can cause up to 80% loss of a grape crop. It can spoil the taste of wine if infected grapes mix with healthy ones.

It''s quite hardy and can survive harsh conditions in canes, leaves, the vine, or the ground.',

'https://www.mpi.govt.nz/biosecurity/pests-and-diseases-not-in-new-zealand/horticultural-pests-and-diseases-not-in-nz/black-rot/',
0),
#6
('Brown marmorated stink bug', 'Halyomorpha halys', 
'Adult BMSB are a brown ‘shield’ shape and about the size of a 10 cent coin.

The easiest way to identify them is from the white bands on their antennae and alternating black and white markings on the abdomen. Its underside is a white/tan colour.

Stink bug eggs are light green, shaped like barrels, and are usually in clusters of 20 to 30.',

'The brown marmorated stink bug (BMSB) is an agricultural, horticultural, and social pest. It''s native to Asia and has spread throughout North America and Europe.

It isn’t established in New Zealand, but this sneaky pest hitchhikes on passengers and imported goods. We’ve caught them at our border many times. We need everyone’s help to keep an eye out for them.',

'The brown marmorated stink bug feeds on more than 300 plant species.  If established in New Zealand it could decimate our fruit and vegetable industries.

During autumn and winter, thousands of bugs can enter houses to shelter from the cold.  When they''re disturbed they release a foul-smelling liquid which can make your house hard to live in.',

'https://www.mpi.govt.nz/biosecurity/pests-and-diseases-not-in-new-zealand/horticultural-pests-and-diseases-not-in-nz/brown-marmorated-stink-bug-threat-to-nz-and-identification/',
0),
#7
('Citrus longhorn beetle', 'Anoplophora chinensis', 
'Both males and females are black and shiny with white to blue spots.

Males are about 21mm long
Females are about 37mm long

Eggs are found singly under bark and are about 6mm long.

The larva (maggot) is:

cylindrical
about 56mm long
10mm wide (at its widest)
without obvious legs
pale yellowish white with a dark head.
Pupae

have long coiled antennae
have legs
are found under bark.',

'This beetle is one of the most destructive pests of fruit trees, especially citrus. It''s native to lowland China and other parts of Asia. It has invaded parts of Europe, including Italy, Turkey, France, Germany, and Croatia.',

'The citrus longhorn beetle feeds on over 100 different host plants, in particular orchard species, like apples and pears. The damage done in orchards can cause serious economic losses, including a decrease in the amount of fruit grown.

The beetle also feeds on many trees found in our urban landscapes, such as alders and plane trees.

The larvae tunnel under the bark, weakening the trees and making them susceptible to disease and wind damage. Young trees are less able to withstand the beetle''s damage.',

'https://www.mpi.govt.nz/biosecurity/pests-and-diseases-not-in-new-zealand/horticultural-pests-and-diseases-not-in-nz/citrus-longhorn-beetle/',
0),
#8
('Laurel wilt and the Asian ambrosia beetle', 'Raffaelea lauricola vectored by Xyleborus glabratus', 
'If a tree is infected, you''ll see wilted leaves that have turned a reddish or purple colour. To start with, it may only affect part of the tree, but it can affect the whole tree. Eventually, the leaves will turn brown, but they tend to stay on the branches.',

'The Asian ambrosia beetle carries the fungus that causes laurel wilt in its mouth parts. The beetle feeds on the fungus. As the beetle tunnels into a tree, it infects the tree with it. 

The beetles mostly live in avocado trees, but can live in several other laurel trees, including bay trees.',

'If laurel wilt established in New Zealand, it would harm our avocado industry.

Laurel wilt invades the tree''s system for carrying water from the roots to the leaves (the vascular system). It blocks the vessels and stops water getting to the leaves. It''s the lack of water that damages the tree.',

'https://www.mpi.govt.nz/biosecurity/pests-and-diseases-not-in-new-zealand/horticultural-pests-and-diseases-not-in-nz/laurel-wilt-and-the-asian-ambrosia-beetle/',
0),
#9

('Medfly (Mediterranean fruit fly)', 'Ceratitis capitata', 
'The adult flies are:

3.5mm to 5mm (slightly smaller than a house fly)
yellowish with a brown tinge
the wings have yellow, brown, and black spots and bands.
A medfly''s wings are distinctive from any other fruit fly.',

'In 1907, we found the medfly in Napier and Blenheim. We managed to destroy those populations. We then introduced stricter biosecurity rules for all fruit imports.

It wasn''t found again until 1995, when we caught a medfly in one of our surveillance traps in Auckland. We successfully eradicated it then too.',

'The adult medfly lays its eggs in fruit. When the maggots hatch they eat the fruit, causing it to rot.

The maggots will eat over 500 different types of fruit and vegetables. Their favourites are apples, pears, stonefruit, citrus, and tomatoes.

This fruit fly is hardier than many other species of fruit fly. As it can withstand the cold better, it could establish in more places within New Zealand.',

'https://www.mpi.govt.nz/biosecurity/pests-and-diseases-not-in-new-zealand/horticultural-pests-and-diseases-not-in-nz/medfly-mediterranean-fruit-fly/',
0),
#10
('Melon fly', 'Zeugodacus cucurbitae', 
'Adult flies:

are 8 to 10mm long
are generally a golden to red-brown colour, sometimes with darker markings
have a dark stripe or T-shaped mark on their abdomen
have wings with a few dark bands or spots
may have a pointed "sting" or ovipositor.
Eggs are laid underneath the skin of the fruit. They hatch into small maggots which leave the fruit when mature, then pupate in soil.',

'The melon fly is native to central Asia but has spread across Asia and into Africa. Although melon fly has been found at our border a few times, it has not been detected inside New Zealand.',

'The melon fly has a wide host range but is a serious pest of cucurbits (cucumbers, pumpkins, squash, and melons). Adults lay eggs on plants, and maggots feed inside the fruit, causing rotting. Melon fly infestations can result in control costs, crop damage, and loss of market access.

Melon fly could survive in the warmer months in much of New Zealand. Populations may be able to establish in warmer parts of the country.',

'https://www.mpi.govt.nz/biosecurity/pests-and-diseases-not-in-new-zealand/horticultural-pests-and-diseases-not-in-nz/melon-fly/',
0);

INSERT INTO Biosecurity (common_name, scientific_name, key_char, biology, impact, source_url, is_present_in_nz) VALUES
#1
('Granulate ambrosia beetle', 'Xylosandrus crassiusculus', 
'Adult Beetle Characteristics
Size: They are small beetles, typically about 2 to 3 mm in length.
Color: Adults are generally dark brown to black.
Body Shape: They have a cylindrical body shape typical of many ambrosia beetles.',

'The granulate ambrosia beetle (Xylosandrus crassiusculus) was detected in Auckland in February 2019. Biosecurity New Zealand has done extensive ground surveys to determine the distribution of the beetles across the Auckland region. The beetle was found in native and exotic species in 7 areas within Auckland. It has not been detected outside the Auckland region.

The Auckland detection was the first time the beetle has been found in New Zealand. However, evidence suggests it may have been in the country for at least 3 years.',

'Biosecurity New Zealand is assessing the potential risk from the beetle to New Zealand native trees and planted trees and shrubs. There is no evidence that any damaging fungi have been transmitted by the granulate ambrosia beetle in New Zealand.',

'https://www.mpi.govt.nz/biosecurity/exotic-pests-and-diseases-in-new-zealand/pests-and-diseases-under-response/granulate-ambrosia-beetle/',
1),
#2
('Pepino mosaic virus (PepMV) ', 'Pepino mosaic virus (PepMV)', 
'Affected plants can show stunted growth or symptoms resembling hormonal herbicide damage. Leaves around the ''head'' of the plant may show dark spots and distortion. Lower leaves may have brown, necrotic lesions.

Other leaf symptoms may be yellow spots which later develop into bright yellow patches on the leaf and ‘bubbling’ on the leaf surface. 

Fruit can appear ''marbled'' and this may be more readily seen on large red tomato varieties.',

'This virus can cause pepino mosaic disease in tomatoes and some other solanaceous plants including potatoes and eggplants.

While the disease can affect production, it has no impact on food safety or human health. Tomatoes are still safe to eat.',

'The disease can affect production',

'https://www.mpi.govt.nz/biosecurity/exotic-pests-and-diseases-in-new-zealand/pests-and-diseases-under-response/pepino-mosaic-virus-pepmv-in-auckland/',
1),
#3
('Potato spindle tuber viroid(PSTVd)', null, 
'PSTVd is a pathogen that causes disease and potential loss of production, mainly in potatoes, tomatoes, pepinos, and capsicum. It can also infect some ornamental plants, including dahlias, chrysanthemums, and petunias.

The viroid has been found twice before in New Zealand in glasshouse tomatoes and capsicum, and in Cape gooseberry. It was eradicated both times.

This plant pest has been found in many parts of the world, including Europe, Central and South America, and Africa.

Many strains of PSTVd exist, with symptoms ranging from asymptomatic to severe infections. The incursion near Nelson, in the Tasman district, appears to be a mild strain of the disease.

A viroid is like a virus but has a simpler structure.',

'The Asian ambrosia beetle carries the fungus that causes laurel wilt in its mouth parts. The beetle feeds on the fungus. As the beetle tunnels into a tree, it infects the tree with it. 

The beetles mostly live in avocado trees, but can live in several other laurel trees, including bay trees.',

'Depending on the strain, PSTVd can affect cropping plants, including potato, tomato, eggplant, and capsicum, potentially reducing crop yields.

Initial introduction of the viroid into potato and tomato crops is mostly through infected seed.

PSTVd is highly contagious. It is transmitted between plants through contact of the sap from small wounds in the leaf of a diseased plant to a healthy plant. This is done through:

touch
cutting or pruning tools
contaminated machinery
aphids from plants also infected with potato leafroll virus
infected potato tubers
pollen, but only to the seeds pollinated, not to the whole plant
potato and tomato true seeds.',

'https://www.mpi.govt.nz/biosecurity/pests-and-diseases-not-in-new-zealand/horticultural-pests-and-diseases-not-in-nz/laurel-wilt-and-the-asian-ambrosia-beetle/',
1),

#4
('Queensland fruit fly eradication', 'Ceratitis capitata', 
'Queensland fruit flies are about 6 to 8 mm long and are reddish-brown with yellow markings.

Larvae look like white long-grain rice.',

'Biosecurity New Zealand mounted a biosecurity response operation after finding a male Queensland fruit fly in a surveillance trap in Northcote in February 2019. Subsequently, a further 9 individual flies were detected in separate traps in the area up to July 2019.

A Controlled Area Notice was put in place, legally restricting the movement of fresh fruit, vegetables, and garden waste out of a specified zone. This was to contain any potential population of the insect pest which would have significantly damaged New Zealand’s horticulture industry and home gardens, had it established here.

After 6 months of trapping without a detection, an intensive baiting programme throughout the spring of 2019, and the inspection of hundreds of kilos of fruit without a find, Biosecurity New Zealand had confidence there was no breeding population of the Queensland fruit fly in Northcote.

The Controlled Area was lifted on 31 January 2020 and operations in the area ceased.',

'Queensland fruit fly would jeopardise our multi-billion-dollar horticulture industry, with 80% of New Zealand’s horticulture crops susceptible to attack.

Fruits and vegetables attacked by Queensland fruit fly are inedible.

Any fruit and vegetables would be subject to trade restrictions.',

'https://www.mpi.govt.nz/biosecurity/exotic-pests-and-diseases-in-new-zealand/pests-and-diseases-under-response/queensland-fruit-fly/',
1),

#5
('Tomato red spider', 'Tetranychus evansi', 
'There are a few red mite species in New Zealand already. Identification requires an expert (acarologist). Lots of webbing is the most obvious sign that the tomato red spider mite is present.',

'The tomato red spider mite feeds on a wide range of plants in the Solanaceae family. In large groups, they can mummify plants, wrapping them up in silk webbing. They will feed on the plant until it dies.

This mite got its name because it eats tomato plants and is red. It makes silk webbing to protect itself and its eggs like some spiders do. But the mite doesn''t just feed on tomatoes.

Find out what else the mites eat

The mite multiplies quickly and can be difficult to control. Many mite species can quickly become resistant to pesticides, which poses challenges for controlling this pest.',

'Biosecurity New Zealand is working with the horticulture industry on assessing the risk this discovery poses. We''re also working on potential next steps.

MPI’s trade and market access specialists have assessed the discovery as unlikely to have any significant impact on trade in horticultural products. The mite is a quarantine pest for Korea, Thailand, and Ecuador. New Zealand does not export substantial host plant products to these countries.

However, we do export some host commodities to Thailand, including tomatoes and strawberries.',

'https://www.mpi.govt.nz/biosecurity/exotic-pests-and-diseases-in-new-zealand/pests-and-diseases-under-response/tomato-red-spider-mite/',
1),
#6
('Brown Marmorated Stink Bug', 'Halyomorpha halys',
'Brown Marmorated Stink Bug (BMSB) adults are approximately 12 to 17 mm in length. They have a distinctive shield shape and are mottled brown in color, with alternating dark and light bands on the edges of their abdomen and across their antennae.',

'The Brown Marmorated Stink Bug is considered a significant threat to New Zealand''s agriculture and horticulture industries. It feeds on more than 300 host plants, including fruits, vegetables, and ornamental plants. The pest can cause severe damage to crops by feeding on fruits and leaves, leading to significant economic losses. It is also a nuisance pest, often seeking shelter in large numbers in houses and other buildings during winter.',

'The presence of BMSB would not only impact crop production but also affect trade, as many countries have strict regulations against importing products from regions infested with the pest. New Zealand has implemented measures to prevent its establishment, including strict biosecurity controls at the border and public awareness campaigns.',

'https://www.biosecurity.govt.nz/protection-and-response/finding-and-reporting-pests-and-diseases/pests/brown-marmorated-stink-bug/',
1),

#7
('Myrtle Rust', 'Austropuccinia psidii',
'Myrtle Rust is a fungal disease that affects plants in the Myrtaceae family. It is easily recognizable by its bright yellow or orange powdery eruptions on leaves, stems, and flowers. The disease can lead to deformed leaves, heavy defoliation of trees, and even death of the plant.',

'Myrtle Rust was first detected in New Zealand in May 2017 and poses a threat to native species such as pōhutukawa, rātā, and mānuka, which are culturally and economically important. The disease spreads rapidly and can be carried long distances by wind, insects, people, and machinery.',

'The impact of Myrtle Rust on New Zealand''s native ecosystems could be devastating, leading to the loss of biodiversity and affecting the health of forest ecosystems. Biosecurity New Zealand is working on disease management strategies, including surveillance, research, and public education, to mitigate its spread and impact.',

'https://www.biosecurity.govt.nz/protection-and-response/finding-and-reporting-pests-and-diseases/pests/myrtle-rust/',
1),

#8
('Varroa Destructor', 'Varroa destructor',
'The Varroa mite is a tiny, reddish-brown parasite that feeds on the bodily fluids of honeybees. Adult mites are about 1.6 mm in length and 1.1 mm in width, making them visible to the naked eye on the bee’s body.',

'This parasitic mite was first detected in New Zealand in 2000 and has since become a significant threat to beekeeping. Varroa mites weaken bees by feeding on them and can spread viruses, notably deforming wing virus. They can cause a collapse of bee colonies, affecting honey production and pollination services.',

'The impact of Varroa mites on New Zealand’s agriculture is significant due to the reliance on honeybees for pollination of many crops. Efforts to control the mite include chemical treatments, breeding Varroa-resistant bees, and biosecurity measures to prevent its spread to the South Island.',

'https://www.biosecurity.govt.nz/protection-and-response/finding-and-reporting-pests-and-diseases/pests/varroa-mite/',
1),

#9
('Giant Willow Aphid', 'Tuberolachnus salignus',
'Giant Willow Aphids are large aphids, measuring up to 6 mm in length. They are dark brown or black and often found in dense colonies on willow trees, sucking sap from the stems and branches.',

'First detected in New Zealand in 2013, these aphids pose a threat to willow trees used for soil conservation, fodder, and amenity purposes. The aphids produce large amounts of honeydew, which can lead to the growth of sooty mold, further weakening the trees. They can also be a nuisance in urban areas due to the sticky honeydew they produce.',

'The presence of Giant Willow Aphids can impact soil conservation efforts and reduce the viability of willow as a fodder crop. Management strategies include monitoring and biological control options, although no fully effective control method has been identified yet.',

'https://www.biosecurity.govt.nz/protection-and-response/finding-and-reporting-pests-and-diseases/pests/giant-willow-aphid/',
1),

#10
('Kauri Dieback', 'Phytophthora agathidicida',
'Kauri Dieback is caused by a microscopic fungus-like organism that infects kauri trees, causing root rot and a collar rot at the base of the tree, leading to the death of the tree. Infected trees show symptoms including yellowing of foliage, loss of leaves, canopy thinning, and lesions that bleed resin.',

'The disease poses a serious threat to New Zealand''s native kauri forests, which are of cultural, ecological, and economic importance. Kauri Dieback was officially identified in New Zealand in 2008, and since then, it has been found in several locations across the North Island.',

'The spread of Kauri Dieback could lead to the decline of kauri forests, significantly impacting New Zealand’s biodiversity and forest ecosystems. Management efforts include public education, track closures, and sanitation stations to prevent soil movement, as there is currently no cure for the disease.',

'https://www.biosecurity.govt.nz/protection-and-response/finding-and-reporting-pests-and-diseases/pests/kauri-dieback/',
1);


INSERT INTO biosecurityimage (biosecurity_id,image_path ,description , is_primary ) VALUES
('1', '11.jpg', ' ', 1),
('1', '12.jpg', ' ', 0),
('1', '13.jpg', ' ', 0),
('2', '21.jpg', ' ', 1),
('2', '22.jpg', ' ', 0),
('2', '23.jpg', ' ', 0),
('3', '31.jpg', ' ', 1),
('3', '32.jpg', ' ', 0),
('3', '33.jpg', ' ', 0),
('4', '41.jpg', ' ', 1),
('4', '42.jpg', ' ', 0),
('4', '43.jpg', ' ', 0),
('5', '51.jpg', ' ', 1),
('5', '52.jpg', ' ', 0),
('5', '53.jpg', ' ', 0),
('6', '61.jpg', ' ', 1),
('6', '62.jpg', ' ', 0),
('6', '63.jpg', ' ', 0),
('7', '71.jpg', ' ', 1),
('7', '72.jpg', ' ', 0),
('7', '73.jpg', ' ', 0),
('8', '81.jpg', ' ', 1),
('8', '82.jpg', ' ', 0),
('8', '83.jpg', ' ', 0),
('9', '91.jpg', ' ', 1),
('9', '92.jpg', ' ', 0),
('9', '93.jpg', ' ', 0),
('10', '101.jpg', ' ', 1),
('10', '102.jpg', ' ', 0),
('10', '103.jpg', ' ', 0),
('11', '111.jpg', ' ', 1),
('11', '112.jpg', ' ', 0),
('11', '113.jpg', ' ', 0),
('12', '121.jpg', ' ', 1),
('12', '22.jpg', ' ', 0),
('12', '123.jpg', ' ', 0),
('13', '131.jpg', ' ', 1),
('13', '132.jpg', ' ', 0),
('13', '133.jpg', ' ', 0),
('14', '141.jpg', ' ', 1),
('14', '142.jpg', ' ', 0),
('14', '143.jpg', ' ', 0),
('15', '151.jpg', ' ', 1),
('15', '152.jpg', ' ', 0),
('15', '153.jpg', ' ', 0),
('16', '161.jpg', ' ', 1),
('16', '162.jpg', ' ', 0),
('16', '163.jpg', ' ', 0),
('17', '171.jpg', ' ', 1),
('17', '172.jpg', ' ', 0),
('17', '173.jpg', ' ', 0),
('18', '181.jpg', ' ', 1),
('18', '182.jpg', ' ', 0),
('18', '183.jpg', ' ', 0),
('19', '191.jpg', ' ', 1),
('19', '192.jpg', ' ', 0),
('19', '193.jpg', ' ', 0),
('20', '201.jpg', ' ', 1),
('20', '202.jpg', ' ', 0),
('20', '203.jpg', ' ', 0);

