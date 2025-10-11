import os
import time

def clear_screen():
    """Clears the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title):
    """Prints a formatted header."""
    clear_screen()
    print("=" * 50)
    print(f"      Jedi Manual - tahkmahnelle edition 7")
    print("=" * 50)
    print(f"\n--- {title} ---\n")

def temple_of_the_jedi_order():
    """Displays the main introduction."""
    print_header("Temple of the Jedi Order")
    print("""
Jediism is a religion based on the observance of the Force, a ubiquitous and
metaphysical power that a Jedi (a follower of Jediism) believes to be the
underlying, fundamental nature of the universe. Jediism finds its roots in
philosophies similar to those presented in an epic space opera called “Star Wars”.
It is a religion in and of itself.

The Jedi religion is an inspiration and a way of life for many people throughout
the world who take on the mantle of Jedi. Jedi apply the principles, ideals,
philosophies and teachings of Jediism in a practical manner within their lives.
Real Jedi do not worship George Lucas or Star Wars or anything of the sort.
Jediism is not based in fiction, but we accept myth as a sometimes more practical
means of conveying philosophies applicable to real life.
    """)
    input("\nPress Enter to return to the menu...")

def jedi_believe():
    """Displays the 'Jedi Believe' section."""
    print_header("Jedi Believe")
    print("""
In the Force, and in the inherent worth of all life within it.
In the sanctity of the human person. We oppose the use of torture and cruel or unusual punishment, including the death penalty.
In a society governed by laws grounded in reason and compassion, not in fear or prejudice.
In a society that does not discriminate on the basis of sexual orientation or circumstances of birth such as gender, ethnicity and national origin.
In the ethic of reciprocity, and how moral concepts are not absolute but vary by culture, religion and over time.
In the positive influence of spiritual growth and awareness on society.
In the importance of freedom of conscience and self-determination within religious, political and other structures.
In the separation of religion and government and the freedoms of speech, association and expression.
    """)
    input("\nPress Enter to return to the menu...")

def three_tenets():
    """Displays 'The Three Tenets' section."""
    print_header("The Three Tenets")
    print("""
When used correctly, the Jedi Tenets allow us to better ourselves and overcome any obstacle.
They help us improve the world around us and fulfil our purpose in life as a Jedi.

- Focus
- Knowledge
- Wisdom

Focus is the art of pruning the irrelevant and pouring the best of your mind into what you are doing.

Knowledge can be acquired by focusing on the task at hand.

Wisdom is the sound application of accrued knowledge and experience through patient, good judgment.
    """)
    input("\nPress Enter to return to the menu...")

def the_code():
    """Displays 'The Code' section."""
    print_header("The Code")
    print("""
The Jedi Code comes in two versions which are different ways of understanding the same teaching.

Emotion, yet Peace.         |   There is no Emotion, there is Peace.
Ignorance, yet Knowledge.    |   There is no Ignorance, there is Knowledge.
Passion, yet Serenity.       |   There is no Passion, there is Serenity.
Chaos, yet Harmony.          |   There is no Chaos, there is Harmony.
Death, yet the Force.        |   There is no Death, there is the Force.

by Greg Costikyan
    """)
    input("\nPress Enter to return to the menu...")

def meditation_for_jedi():
    """Displays 'A Meditation For Jedi' section."""
    print_header("A Meditation For Jedi")
    print("""
I am a Jedi, an instrument of peace;

Where there is hatred I shall bring love;
Where there is injury, pardon;
Where there is doubt, faith;
Where there is despair, hope;
Where there is darkness, light;
And where there is sadness, joy.

I am a Jedi.

I shall never seek so much to be consoled as to console;
To be understood as to understand;
To be loved as to love;
For it is in giving that we receive;
It is in pardoning that we are pardoned;
And it is in dying that we are born to eternal life.

The Force is with me always, for I am a Jedi.


adopted from the Prayer of St. Francis of Assisi, author unknown, 1915.
    """)
    input("\nPress Enter to return to the menu...")

def sixteen_teachings():
    """Displays 'The 16 Teachings' section."""
    print_header("The 16 Teachings")
    print("""
1. Jedi feel the Force. We are aware of its omnipresence and its flow. We endeavour to live in balance with it as it manifests in all worldly phenomena, the dynamic equilibrium of its flow which transcends space-time from the smallest quark to the greatest expanse of the cosmos. Living in balance with The Force is the core value of a Jedi.

2. To be in balance, the Jedi practise clarity of mind. Aware that representations of the world can cloud our understanding, the Jedi centre their awareness through the practice of meditation and contemplation.

3. Jedi maintain a clarity of awareness that all events are interconnected. The balance of the Force is a flowing continuum; it flows around us and through us, allowing us to adapt to change arising in its eternal cycles of creation and renewal.

4. Jedi practise non-attachment, maintaining an awareness that the cycles of creativity and renewal in the Force give rise to phenomena as others pass away.

5. Jedi comprehend that we are beings of thought, feeling, and will, who flourish within the Force through self-aware action and lifelong learning.

6. The Jedi practise humility. Jedi know that we are processes in The Force and exist within its cycles of creativity and renewal. The more we practise humility, the more open we become to insights of wisdom which come to us through our feeling of the Force.

7. The Jedi foster an acceptance of limitations. To change the world is to change our perceptions of and perspectives towards it. Indeed, we are capable of amazing acts, especially when we rely on the flow of the Force. Yet, as incarnated, organic beings we must understand that the power is that of the Force, without which we are mere matter.

8. The Jedi practise patience. All creation and renewal in the flow of the Force, all the wonder and terror of its processes, arise and dissolve in eternity – the present moment, the now. With the practice of acceptance and patience, Jedi have the tenacity to attend with curiosity to the phenomena in our experience which proceed one from another, ad infinitum.

9. The Jedi maintain integrity, our individuated wholeness. We practise to foster the awareness of our interconnection with all other phenomena, thus ensuring authenticity in our interactions with others and our capacity to accept our limitations and those in interaction with us.

10. The first and foremost service a Jedi performs is devotion to our learning. Only by curating our individuated, authentic, whole being-ness, can we serve in more collaborative ways, participating in the creative, renewing flow of the Force. With our devotion to the discipline of universal compassion in the Force, we embody the source of love and harmony we bring into the world.

11. The Jedi practise living in universal compassion, understanding the phenomena of our environment. We cultivate a particular sensitivity to when feelings of fear, anger, hatred, and aggression germinate within us. These emotions are among our limitations as incarnated, organic beings. We bring to these feelings hope, pardon, and love in equal measure to bring us back into balance with the movement of the Force.

12. Unconditional love and compassion are central in the life of the Jedi. Where imbalance arises, we bring only so much love, pardon, faith, hope, clarity, and joy as is necessary to restore the dynamic equilibrium in our phenomenal environment.

13. The Jedi cultivate empathy with others. Maintaining a keen sensitivity to when the feelings of fear, anger, hatred, and aggression move within us, we empathically and compassionately comprehend how these feelings also arise in others. Those whom we perceive as adversaries also share these limitations. With this understanding, we respond to imbalance so as to return harmony to the flow of interactions.

14. The Jedi seek to return balance to that which has become tumultuous. Pain is one of the few real things we have access to, and as such, we are dedicated to alleviating it insomuch as is within our limitations. The clarity of understanding we cultivate permits us to know how and when to offer help to those in need and gives us the courage to do so.

15. The Jedi realise that all phenomena, including that of life itself, arise from and dissolve back into the cycles of creation and renewal of the Force. We are aware of the interconnectedness and the continuum of all phenomena, that unconditional love and compassion are central to us, and that pain is real. When we must bear witness to the dissolution of those we care for in our and their limited, incarnated, organic capacity, we must extend our compassion, our faith, and our comprehension to re-balance that which we otherwise would feel as loss. The Force only creates and renews, it does not deprive.

16. Following All the Teachings offered here, and as witnessed by the thousands of generations who have come before us, the Jedi must have the deepest commitment, the most sincere soul. These teachings are difficult to practise, but their benefits are great. With continuous training, centring and balancing meditation, humble understanding, and receptivity, we may participate in the experience of being alive more fully, more harmoniously, and more creatively. Then we may return into the Force from which we have come by the same integrity with which we have lived. In this way, our Spirit will go forth, bringing balance through love, pardon, faith, hope, light, and some joy to generations yet to come.
    """)
    input("\nPress Enter to return to the menu...")

def twenty_one_maxims():
    """Displays 'The 21 Maxims' section."""
    print_header("The 21 Maxims")
    print("""
1.  Training - The purpose of training is to accommodate error without consequence. It is the key to learning and the Jedi Teachings are hazardous without guided practice.
2.  Teaching - Love what you teach and love who you teach. Teachers affect eternity - who can tell where their influence stops ? The Jedi mentor is there to challenge the learner, but never to pose an obstacle to their progress.
3.  Discipline - A disciplined mind will lead to peace, an undisciplined mind will lead to suffering. Indeed, for the mind without discipline, the Jedi Way will be impassable.
4.  Dedication - Inspiration lasts a week, motivation will fade after a month, disciplined dedication lasts a lifetime. The way to do great work is to love what you do and who you work with.
5.  Meditation - You have a treasure within you. The key to this treasure is meditation. It is not evasion, meditation fosters a serene confluence of the symbolic with the imaginary : reality. To the Jedi with a quiet mind, The Force will be felt and It will inform us.
6.  Clear Intention - The Force follows intentionality. With a quiet mind, we direct our clear intention through the ocean of possibilities and allow The Force to work through us.
7.  Balance - When we allow peace, harmony, and balance in our minds, The Force manifests in the world. In art and dream, we may proceed with abandon. In waking life shared with others, we must proceed with balance and discretion.
8.  Humility - Our perpetual trial is humility. We understand our agency is not solely from us, but through us : it is of The Force. In feeling The Force in ourselves, we see It in everyone and everything.
9.  Agency - Jedi are active in the world, acting as people of thought, and thinking like people of action. Be aware that beliefs become thoughts, thoughts become words, words become actions, actions become habits, habits become values, and values determine destiny.
10. Capability - The Force does not ask of our ability, only our availability. In opening to The Force, Its capabilities flow through us. Indeed, clear intention is not enough, Jedi do.
11. Self-Control - To control intention, the Jedi use The Force to tame the passions. In self-control lies the seed of freedom. We work to control our passions, lest someone exploit us through them.
12. Discretion - For the Jedi, discretion is the better part of valour. Indeed, agency without discretion comes invariably to a tragic end. True wisdom is found in knowing when to raise the eyebrow, rather than the voice or the sword.
13. Integrity - Taking the right action even when nobody's watching, integrity is easier kept than recovered. There is no such thing as a minor lapse of integrity.
14. Fairness - The ability to rise above prejudice, all virtue is summed up in fairness. Indeed, lack of fairness is essentially a mark of weakness.
15. Charity - In brightening everything on which it shines, Charity is love in action. We live on what we are given but build our lives on what we give.
16. Compassion - Via compassion, The Force exhibits its true power. In seeking peace for others we practice compassion, in seeking peace for ourselves we practice compassion.
17. Empathetic Joy - The necessary counterbalance to compassion, empathetic joy prevents the waters of compassion from draining away. We aim to feel the joy of others just as keenly as their pain.
18. De-escalation - Between uncontrolled escalation and passivity, there is a demanding path of responsibility that we follow. Whenever we perceive monsters we should see to it we do not become monsters ourselves.
19. Valour - True valour lies between cowardice and rashness. It is a delicate skill, those having it never knowing for sure until the trial comes. In any case, valour that struggles is better than recklessness that thrives.
20. Honour - Acting with honour through The Force preserves peace. Always remember : if peace cannot be maintained with honour, it is no longer peace.
21. Decency - Through decency, we render happenings tolerable. Decency is not derived through faith but precedes it. If decency could be easily found in reality, would we have need of myth ?
    """)
    input("\nPress Enter to return to the menu...")

def doctrine_menu():
    """Displays the doctrine sub-menu."""
    while True:
        print_header("Doctrine of the Order")
        print("1. Jedi Believe")
        print("2. The Three Tenets")
        print("3. The Code")
        print("4. A Meditation For Jedi")
        print("5. The 16 Teachings")
        print("6. The 21 Maxims")
        print("7. Back to Main Menu")

        choice = input("\nEnter your choice (1-7): ")

        if choice == '1':
            jedi_believe()
        elif choice == '2':
            three_tenets()
        elif choice == '3':
            the_code()
        elif choice == '4':
            meditation_for_jedi()
        elif choice == '5':
            sixteen_teachings()
        elif choice == '6':
            twenty_one_maxims()
        elif choice == '7':
            break
        else:
            print("Invalid choice, please try again.")
            time.sleep(1)

def main_menu():
    """Displays the main menu of the application."""
    while True:
        print_header("Main Menu")
        print("1. Temple of the Jedi Order (Introduction)")
        print("2. Doctrine of the Order")
        print("3. Exit")

        choice = input("\nEnter your choice (1-3): ")

        if choice == '1':
            temple_of_the_jedi_order()
        elif choice == '2':
            doctrine_menu()
        elif choice == '3':
            clear_screen()
            print("\nMay the Force be with you.\n")
            break
        else:
            print("Invalid choice, please try again.")
            time.sleep(1)

if __name__ == "__main__":
    main_menu()

