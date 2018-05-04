# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from setup import BooksS, BookSection, User, Base

engine = create_engine('sqlite:///BooksCatalogwithusers.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Create dummy user
user1 = User(name="Lucy Williams", email="satyachalasani7@gmail.com",
             picture='http://1onjea25cyhx3uvxgs4vu325-wpengine.netdna-ssl.com/wp-content/uploads/2016/02/U_360x360px.jpg')
session.add(user1)
session.commit()


# BOOKS UNDER DRAMA
category1 = BookSection(name="DRAMA", user_id=1)

session.add(category1)
session.commit()

Books1 = BooksS(user_id=1,name="Romeo and Juliet", description="Capulet tells Paris that he may not marry his daughter Juliet until she is Romeo and his friends learn of a party being held by the Capulets, and decide to go to it as masquers.At the party, Tybalt sees Romeo, but is prevented from fighting him byCapulet Romeo meets Juliet Romeo meetsJuliet, and they instantly fall in love.", price="$9.50", rating = "Excellent", Sections=category1)

session.add(Books1)
session.commit()



Books2 = BooksS(user_id=1, name= "A Dolls House", description="for the first time portrayed the tragic hypocrisy of Victorian middle class marriage on stage he play ushered in a new social era and exploded like a bomb into contemporary life.", price="$4.25", rating = "Excellent", Sections=category1)

session.add(Books2)
session.commit()

Books3 = BooksS(user_id=1, name="Daddy's Girl", description="After Don Mitchell (William Katt) and his Barbara (Michele Greene), adopt young Jody (Gabrielle Boni), the little girl becomes particularly attached to her new father, and eventually utterly obsessed. As a result, Jody's psychotic tendencies emerge in a variety of violent ways. Before long, people who are close to Don begin to die in rapid succession,and his niece, Karen (Roxana Zal), who suspects Jody's involvement, starts to investigate the youngsters past.", price="$9.50", rating = "veryGood",  Sections=category1)

session.add(Books3)
session.commit()


# BOOKS UNDER FICTION
category2 = BookSection(name="FICTION", user_id=1)

session.add(category2)
session.commit()

Books1 = BooksS(user_id=1, name="Little Fires Everywhere",  description="Mia starts as Mrs. Richardon's tenant, then becomes her housekeeper,then a mentor and secret keeper for her children; Pearl falls into a love triangle with the two Richardson boys.Like Shaker Heights,Little Fires Everywhere is meticulously planned,every storyline and detail placed with obvious purpose", price="$5.50", rating = "veryGood", Sections=category2)

session.add(Books1)
session.commit()

Books2 = BooksS(user_id=1, name="The Great Gatsby",  description="The Great Gatsby is a story told by Nick Carraway, who was once Gatsby's neighbour and he tells the story sometime after 1922, when the incidents that fillthe book take place.As the story opens, Nick has just moved from the Midwest to West Egg, Long Island, seeking his fortune as a bond salesman.", price="$7.99", rating = "Good", Sections=category2)

session.add(Books2)
session.commit()

Books3 = BooksS(user_id=1, name="The Lord of the Rings",   description="The future of civilization rests in the fate of the One Ring,which has been lost for centuries. Powerful forces are unrelenting in their search for it.But fate has placed it in the hands of a young Hobbit named Frodo Baggins (Elijah Wood),who inherits the Ring and steps into legend. A daunting task lies ahead for Frodo when he becomes the Ringbearer to destroy the One Ring in the fires of Mount Doom where it was forged.", price="$6.95", rating = "Excellent", Sections=category2)

session.add(Books3)
session.commit()                     

Books4 = BooksS(user_id=1, name="Beloved",  description="Beloved begins in 1873 in Cincinnati, Ohio, where Sethe, a former slave, has been living with her eighteen-year-old daughter Denver. Sethe's mother-in-law, Baby Suggs,lived with them until her death eight years earlier. Just before Baby Suggs's death, Sethe'two sons, Howard and Buglar, ran away." , price="$1.99", rating = "Excellent", Sections=category2)


session.add(Books4)
session.commit()

# BOOKS UNDER SUSPENCE
category3 = BookSection(name="SUSPENCE", user_id=1)

session.add(category3)
session.commit()

Books1 = BooksS(user_id=1, name="Before I Go to Sleep", description="Ever since a vicious attack nearly claimed her life Christine Lucas (Nicole Kidman) has suffered from anterograde amnesia and is unable to form new memories. Every morning, she becomes reacquainted with her husband, Ben (Colin Firth) and the other constants in her life. In accordance with her doctor's (Mark Strong) instructions Christine keeps a video diary. As Christine starts to uncover terrifying truths about her past, she begins to question everything -- and everyone -- around her.", price="$3.95", rating = "veryGood",  Sections=category3)

session.add(Books1)
session.commit()

Books2 = BooksS(user_id=1, name="Gone Girl",   description="In Carthage, Mo., former New York-based writer Nick Dunne (Ben Affleck) and his glamorous wife Amy (Rosamund Pike) present a portrait of a blissful marriage to the public. However, when Amy goes missing on the couple's fifth wedding anniversary, Nick becomes the prime suspect in her disappearance. The resulting police pressure and media frenzy cause the Dunnes'image of a happy union to crumble, leading to tantalizing questions about who Nick and Amy truly are.",  price="$7.99", rating = "veryGood",  Sections=category3)

session.add(Books2)
session.commit()

Books3 = BooksS(user_id=1, name="Pretty Girls Dancing",   description="Pretty Girls Dancing Kindle Edition. Years ago,in the town of Saxon Falls,", price="$13.95", rating = "veryGood", Sections=category3)

session.add(Books3)
session.commit()


# BOOKS UNDER COMEDY
category4 = BookSection(name="COMEDY", user_id=1)



session.add(category4)
session.commit()

Books1 = BooksS(user_id=1, name="Bossypants",  description="Before Liz Lemon, before Weekend Update,before Sarah Palin,Tina Fey was just a young girl with a dream: a recurring stress dream that she was beingchased through a local airport by her middle-school gym teacher.She also had a dream that one day she would be a comedian on TV.", price="$8.99", Sections=category4)


session.add(Books1)
session.commit()

Books2 = BooksS(user_id=1, name="Girl Logic",  description="Girl Logic is Iliza's term for the way women obsess over details and situations that men don't necessarily even notice. She describes is as a characteristically female way of thinking that appears to be contradictory and circuitous but is actually a complicated and highly evolved way of looking at the world. When confronted with critical decisions about dating, sex, work, even getting dressed in the morning, Iliza argues that women will by nature consider every repercussion of every option before making a move toward what they really want.And that kind of holistic thinking can actually give women an advantage in what is still a male world.", price="$10.95", rating = "Good", Sections=category4)
session.add(Books2)
session.commit()


Books3 = BooksS(user_id=1, name="I Can't Make This Up",  description="It begins in North Philadelphia.He was born an accident.unwanted by his parents. His father was a drug addict who was in and out of jail.His brother was a crack dealer and petty thief. And his mother was overwhelmingly strict, beating him with belts, frying pans, and his own toys.", price="$8.95", rating = "Average", Sections=category4)

session.add(Books3)
session.commit()


categories = session.query(BookSection).all()
for BookSection in categories:
    print ("BookSection: " + BookSection.name)
