#just a place to store our dictionary for the fetchables game.

class Fetchables:
    def __init__(self):

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
    
    #a function to tally the total probability to verify it is 1.
    def check_probs(self):
        
        #iterate through each dictionary of values and add the probability attribute for each.
        total_probability = 0
        for value in self.fetchables.values():
            total_probability += value['probability']

        #return the result. If valid, it should be exactly 1.
        return total_probability


#run this file to verify the probability is correct
if __name__ == '__main__':
    fetchables = Fetchables()
    print(fetchables.check_probs())