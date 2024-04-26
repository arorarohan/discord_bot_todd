#just a place to store our dictionaries of items, so they don't take up too much space in the cogs where they are used.

class Dictionaries:
    
    #call this if we want our fetchables
    def load_fetchables(self):
        self.fetchables = {
            'stick': {
                'probability': 0.15,
                'value': 1,
                'image': 'assets/fetch/stick.png',
                'message': 'Woof! Todd just found a stick! Good boy!'
            },
            'ball': {
                'probability': 0.13,
                'value': 1,
                'image': 'assets/fetch/ball.png',
                'message': 'Bark! Todd just found a ball! In the distance, you see exasperated tennis players yelling slurs at Todd. Good dog!'
            },
            'rat': {
                'probability': 0.11,
                'value': 2,
                'image': 'assets/fetch/rat.png',
                'message': 'Oh no! Todd just found a rat! Looks like it\'s only just died. Todd grins maniacally, a murderous look in his eyes, and wags his tail furiously. Attaboy!'
            },
            'spider in a jar': {
                'probability': 0.05,
                'value': 7,
                'image': 'assets/fetch/spider_in_a_jar.png',
                'message': 'Todd wandered off into the New Mexico desert and returned with a spider in a jar. He seems emotionless and stoic, as if his mind is still out there among the dunes. I wonder what he saw...'
            },
            'nothing': {
                'probability': 0.11,
                'value': None,
                'image': None,
                'message': 'Todd searched far and wide, and came back empty-handed. You call him a bad dog and storm off, but Todd whimpers and follows you closely. He may not be smart, but he sure is loyal.'
            },
            'face of god': {
                'probability': 0.005,
                'value': None,
                'image': 'assets/fetch/face_of_god.png',
                'message': 'Todd stumbles back to you. Initially, you think he just failed to find anything and came back quickly, but then you look closer into his eyes. They seem to be hollow, soulless, like he\'s seen something he cannot describe to you. "I saw the face of God," Todd said, "A distant vision from behind the clouds. The heavenly bells and choir sounded, rang in my ears, a cacophony of holiness I was unfit of witnessing. His Eye watched me, judging me." Todd shivers. "I dare not envision it even now, lest I fall back into despair. What felt like seconds for you was years for me. The bells still ring. I fear they will continue to ring till I am gone. And when the last of my ashes is incinerated, and the universe breathes its last, that unceasing melody will only get louder."'
            },
            'gold': {
                'probability': 0.02,
                'value': 50,
                'image': 'assets/fetch/gold.png',
                'message': 'Bark! Yap! Run in circles! Jubilation! Todd just found a bar of gold! He drops it and it lands squarely on your big toe, and you convulse in pain on the ground, grinning with pride as Todd licks your face enthusiastically.\nYour score has been inducted into the hall of fame! Use <todd hall_of_fame> to see high scores.'
            },
            'briefcase': {
                'probability': 0.08,
                'value': 4,
                'image': 'assets/fetch/briefcase.png',
                'message': 'Hmm... Todd just found a strange, black briefcase. Maybe best not to open it for now.'
            },
            'skull': {
                'probability': 0.08,
                'value': 4,
                'image': 'assets/fetch/skull.png',
                'message': 'Todd comes trotting up to you with a human skull!'
            },
            'your mother': {
                'probability': 0.06,
                'value': 5,
                'image': 'assets/fetch/your_mother.png',
                'message': 'Todd yelps and comes whimpering back. He found your mother! She sends you both back to your room, but some coins fall out of her pocket as she turns away.'
            },
            'frisbee': {
                'probability': 0.065,
                'value': 6,
                'image': 'assets/fetch/frisbee.png',
                'message': 'Look at that! Todd has fetched a frisbee! he holds it up to you gleefully. You throw it, and todd races forward, leaping into the air to catch it. For a moment, everything feels right in the world.'
            },
            'old sock': {
                'probability': 0.06,
                'value': 8,
                'image': 'assets/fetch/old_sock.png',
                'message': 'Todd returns proudly with an old, smelly sock. You laugh, wondering where he found it, but his wagging tail tells you he thinks it\'s the best thing ever. Either way, you know he\'s going to need his teeth brushed now. Oh well.'
            },
            'diamond ring': {
                'probability': 0.02,
                'value': 30,
                'image': 'assets/fetch/diamond_ring.png',
                'message': 'Todd comes back seemingly empty-handed, but he can\'t contain his excitement. He\'s barking desperately while running in circles! Just as you\'re starting to wonder what the fuss is about, todd squats down and starts taking a poop. You open your mouth to start scolding him, but his eyes say \"trust me!\" He steps away from his fresh turd, and the glint of something shiny catches your eye. You look closer. Unbelieveable! Todd had swallowed a **diamond ring!**'
            },
            'rubber chicken': {
                'probability': 0.06,
                'value': 8,
                'image': 'assets/fetch/rubber_chicken.png',
                'message': 'Todd trots back with a brand-new rubber chicken in his mouth, squeaking it enthusiastically. He drops it at your feet, seeming genuinely proud of his discovery. Oh, todd. What a silly little dog.'
            }
        }
        return
    
    #and call this if we want our shop items
    def load_shop_items(self):
        self.shop_items = {
                'collar':{
                    'value':50, 
                    'message':'you put a nice new bright red collar around todd! he licks your hands. he seems to like it!', 
                    'image':'assets/use/collar.png'
                    },
                'pickle':{
                    'value':20, 
                    'message':'you show todd your pickle. he sniffs it, sneezes on it, then backs away, as if to say: \"What made you think I would want to eat that?\" Maybe he would prefer some treats?', 
                    'image':'assets/use/pickle.png'
                    },
                'leash':{
                    'value':35, 
                    'message':'you clip a nice new bright red leash onto todd\'s collar! todd gnaws at in in disapproval. He doesn\'t like being confined, but who does? At least this way, you know he\'ll be safe when you go out together.', 
                    'image':'assets/use/leash.png'
                    },
                'bag_of_treats':{
                    'value':70, 
                    'message':'you open up a brand new bag of treats! Todd smells it and comes running. You feed him one, and he swallows it without even chewing, his mind already obsessed with the possibility of getting another one. You close up the bag. \"You can\'t have too much of a good thing\", you tell him.', 
                    'image':'assets/use/treats.png'
                    },
                'todd_dna_test':{
                    'value':90, 
                    'message':'the $5 dog DNA test kit you ordered online has finally arrived! You open it up and swab a reluctant todd\'s nostril. \"Let\'s find out where you came from\", you say to him. You dip the swab in the mixture, then pour it onto the test strip. As the blue liquid spreads, a message begins to appear. \"Your dog is 100 per cent adorable!\". You didn\'t have high expectations, but man. What a rip off.', 
                    'image':'assets/use/dna_kit.png'
                    },
                'squeaky_toy':{
                    'value':100, 
                    'message':'it\'s todd\'s birthday! You toss him the new toy you bought for him - a squeaky ball! Todd catches it and starts running around the house, squeaking it repeatedly. An hour later, he still hasn\'t stopped. You\'re starting to regret this.', 
                    'image':'assets/use/squeaky_toy.png'
                    },
                'golden_statue':{
                    'value':500, 
                    'message':'Finally, It is complete. Your specially-commissioned golden statue of todd! It glistens magnificently. You let todd sniff it. He decides it is not edible. Unimpressed, he trots away.', 
                    'image':'assets/use/golden_statue.png'
                    },
                'dog_training_book':{
                    'value':150, 
                    'message':'You\'ve purchased a dog training book from a garage sale! Finally, todd will learn some tricks. You open it, eager to start. Unfortuntely, it seems you\'ve been conned! This book has nothing to do with dogs.', 
                    'image':'assets/use/dog_training_book.png'
                    },
                'stuffed_panda':{
                    'value':200, 
                    'message':'you show todd the stuffed panda you got him! He gently takes it from your hands, brings it to the corner where he sleeps, and sets it down. Who knew even dogs liked stuffed toys?', 
                    'image':'assets/use/panda.png'
                    },
                'staff_of_todd':{
                    'value':250, 
                    'message':'Behold! The staff of todd! Magnificent! Wait, hold on... This looks just like the stick todd found in the park the other day! Did they just really resell it to you for 250x its worth? Well, todd\'s absolutely ecstatic about it, so I guess that\'s a win?', 
                    'image':'assets/use/staff_of_todd.png'
                    },
                'immortality':{
                    'value':4200, 
                    'message1':'You feel your weight beginning to decrease. Not just physically; the weight of the world itself is coming off your shoulders. You\'re gaining a new perspective on life. You think back to the past and realize your memory is limitless; your understanding of time is no longer a linear concept that begins when you were born and ends when you die. It extends far further than that, and in all directions - time is a fabric, a cloth so large it reaches far beyond your ability to comprehend it. It dawns on you that every thread is a soul, a universe in its own right, a lived experience of the individual it belongs to, and between every intersection is a lifetime. You wonder how long your thread is - how many lives you have lived before this one, and how many there will be after it.', 
                    'message2':'It is as you form this thought that you begin to realize something - a feeling that your very concept of self is losing its meaning as rapidly as you rise off the ground. It is not that you have lost any of the individual that you were - it is still there, but there is nothing special about it now. It is just a thread, one of infinitely many, all of which you are rapidly gaining the ability to understand. Not only do you know everything that all beings have ever known, you know them intimately, as though you lived those experiences yourself. It occurs to you that you have. Every thread, every fibre, every intersection - they are all you.',
                    'message3':'You attempt to move your arms, wondering if they still exist, or they too were just a worldly concept which you have ascended beyond. You feel them moving, but they feel different. You hold them out in front of you, and discover that for each feeble, pointless human arm you had, you have sprouted three more. This should feel alien, but you can move them independently like you always could – in every lifetime and in every thread. With these arms, through your fingers, you can control all of them. Every infinitesimal point on the fabric of time itself bends to your will. Every life, every being, every moment. They are all yours now. They always have been. They always will be.',
                    'image':'assets/use/immortality.png',
                    },
                }
        return