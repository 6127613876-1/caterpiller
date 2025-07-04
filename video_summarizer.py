from flask import Flask, render_template_string, request, send_file
import google.generativeai as genai
import os, json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash")

app = Flask(__name__)
SUMMARY_DIR = os.path.abspath("summaries")
os.makedirs(SUMMARY_DIR, exist_ok=True)

# Full video data with transcripts
video_data = {
    "wheel_tractor": [
{
        "video_id": "8EZnuiyoyX8",
        "title": "Cat® Wheel Tractor Scrapers | Improved Features",
        "url": "https://www.youtube.com/watch?v=8EZnuiyoyX8",
        "duration": 162,
        "transcript": "[Music] [Music] hi I'd like to introduce you to the allnew 621 623 and 627h wheel trctor scrapers completely redesigned with the customer of Mind lowering the cost to move a bank cubic yard of dirt let's go up and take a look at the brand new cab and show you some of the improved features that we've got for you this is our brand new cab 21% larger in volume than the G Series completely redesigned a lot more glass and visibility throughout the whole machine you can see much better to the front and down to the left than what you could in the G Series the steering column and pedals foot pedals have been rotated to a line so that the seat when the seat is 30° rotated when you're operating the machine it's a better ride for you we've got a waves module camera uh display up front here it gives you visibility to three different parts of the machine the right hand side The Cutting Edge and the rear of the machine we've got the cluster display all the gauges that you need to see to operate the machine then you have the cat Aug grade GPS technology have a new T handle control for the implements it's got the sequence assist and load assist features built into it there's a button pad here that controls the sequence assist and load assist what the sequence assist and load assist allow you to do is push button load the machine it takes away 14 of the operators normal movements and condenses them down to the push of a button four times to get through the entire sequence load assist allows you to dig automatically where you're just pushing on the throttle and steering the machine making sure it's going next I'd like to talk about the scraper Bowl we've increase the size capacity by 9% it's grown from 22 cubic yards to 24 cubic yards on the 621 and 627 the fuel tank is also grown to give a 10-hour workday without refueling we've made improvements to the cushion hitch to give a better ride for the oper the Hydraulics we moved to Piston Pumps as well as second generation eh Implement controls gives us the multifunctionality to be able to operate the implements simultaneously all that together as well as the other things I've talked about and numerous other things that haven't been mentioned have improved the machine dramatically we have listened to the customer we hope you feel like we've done a good job lowering the cost to move a b cubic yard of dirt if you have more questions please see your local dealer to get those answered we go to production in July 2011 and we look forward to your business"
        },
        {
            "video_id": "Ax6XTAjtvyc",
            "title": "Wheel Tractor Scraper CAT® K Series",
            "url": "https://www.youtube.com/watch?v=Ax6XTAjtvyc",
            "duration": 139,
            "transcript": "null"
        },
        {
            "video_id": "j6CQDwf5F3s",
            "title": "K Series Scrapers Features &amp; Benefits",
            "url": "https://www.youtube.com/watch?v=j6CQDwf5F3s",
            "duration": 527,
            "transcript": "hi I'm Steve Shannon caterpillar will tractor scraper application specialist with the GCI load and haul marketing team let's take a closer look at these productive machines they are unique all-in-one excavating and hauling system they offer lower cost and higher productivity than other load and haul systems when moving high volumes of uniform materials over short to medium distances scrapers can load themselves call at speeds up to 35 mile per hour and unload quickly spreading loads evenly with no need for a dozer today's k-series wheel tractor scrapers feature automated cycle functions high pressure steering engine over speed protection fuel economy mode payload monitoring and other innovations that simplify operation reduce maintenance and boost production configurations include single engine open bowl for long hauls elevating scrapers for work alone capability on flat hauls that double as an excellent finishing tool twin engine powered open bowl scrapers for steep grades and high rolling resistance conditions [Music] let's take a look at some of the features of the newly designed cap k-series caps have improved operator comfort and visibility with redesigned - area monitor and control pad placement it's a 21% larger cap than the G Series operator sound level is 76 DBA Bowl visibility is enhanced with the seat angled at 30 degrees automatic temperature control for operator comfort the standard Kat advanced ride management seat dampens shocks for a smooth comfortable ride and reduced operator fatigue scraper operations are highly productive sequence assistant payload estimator help keep the operator focused on getting to the cut and the film while automating multiple implement movements and keeping track of cycles and payload optional cat great control is available on the k-series scrapers sequence assist is an option on k-series scrapers that combine software and position sensing cylinders to complete tasks for the operator sequence assists can be programmed with the operators preference for bowl and apron height in total it automates 14 manual commands down to 4 pushes of a button load Hall dump and return including control of the cushion hitch transmission hold feature and ejector payload estimator is included with the sequence assist system and will calculate the payload of the machine in tonnes by measuring the bowl lift cylinder pressures at the beginning of the loaded haul segment cat great control automates the bowl height to ensure the machine does not cut below grade or overfill in the dump area avoiding excess material movement and rework k series scrapers have more capacity and increased speed for more cycles and higher productivity [Music] we have incorporated new safety features with both the operator and the job site in mind the optional waves work area vision system is a closed-circuit video system that is designed to enhance the operators view during machine operation waves is equipped with a rear mounted camera a cutting-edge camera a right side mounted camera and the monitor in the cab the operator can toggle between the different camera views from the key panel optional LED lighting enhances visibility allowing for operating during night shifts standard access ladder for cab entry and exit an optional remote access ladder system can be easily activated from ground level and the operator cab speed control is used when the top speed must be limited in short segments of the hall or for intermediate periods of time the operator can set the desired top speed and the machine selects the appropriate gear for conditions tractor and scraper cat engine brakes are controlled by a three-position retarder lever on the steering column for safer operation going down hill additional features and benefits that ensure higher efficiency and ease of operation include an advanced cushion hitch connect the tractor with the gooseneck of the scraper when activated it cushions and smooths the ride even with a loaded ball and at full speed nitrogen over oil accumulators together with advanced software prevent end stroke events and absorb and dampen road shock this improves hitch light and reduces a repair and maintenance cost with improved ride for operators in rough conditions locking down the cushion hitch provides positive cutting edge down pressure in the cut or wild grading draft arm overflow guards on open ball scrapers are now standard to help prevent material coming over the ball sides and lodging between the bowl and draft arms fuel economy mode is a two-part feature when selected the first part of the feature lowers the transmission shift points allowing shifting to take place at lower rpms to aid in fuel savings the second part allows the machine when operated at engine RPMs less than full throttle to automatically vary the power distribution between the tractor and the scraper allowing the machine to utilize the more efficient tractor powertrain versus the full time torque converter drive scraper powertrain engine over speed protection automatically senses engine over speed conditions based on the rate of acceleration and applies the compression brake or service brakes automatically high-pressure steering requires less steering effort resulting in less operator fatigue that helps to keep the production steady throughout the ship tractor and scraper ICI PC transmission controller provides smooth shifts at speed and under full load differential lock engagement protection prevents the operator from engaging the differential lock when damage could occur tire spin reduction and advanced tire spin reduction will allow the machine to control the slip of the tractor tires and wheel spin by adjusting engine RPMs with no additional operator input cab air intake pre cleaner is standard and serviceable at ground level wet disc brakes for long life and dependability improve tractor surface ability with the filter Bank located at ground level access on the right hand side of the machine [Music] [Music] catapillar wheeled tractor scrapers are excellent for moving large volumes of material and provide high potential for profit in the right applications the features benefits and construction of today's wheeled tractor scrapers contribute to low cost per yard accomplished through fast haul speeds efficient loading and quick controlled dumping it's not how much you fit in the ball it's how often you fill it visit your local caterpillar dealership and talk to their earthmoving specialists on how to incorporate scrapers into your next project [Music]"
        },
        {
            "video_id": "YYc9PlEAkkE",
            "title": "Wheel Tractor Scraper CAT® 631K C202",
            "url": "https://www.youtube.com/watch?v=YYc9PlEAkkE",
            "duration": 227,
            "transcript": "[Music] the connect to or to project is filled to alleviate a lot of freeway congestion in downtown Phoenix the freeway will connect on the west side of the valley at 59th and i-10 and then it will connect more south of Phoenix near i-10 and Pecos the total length of the freeways approximately 22 miles currently on the connect 202 project most of the equipment is majority cat equipment we currently have five 631 k.will tractor scrapers and we also have three 623 k scrapers and then we do have five more 623 k scrapers throughout the 202 project the 631 KS have an out to 202 project now for about three months I know that they're getting great production out of the 630 ones down time for the brand-new machines has been very very minimal and I can definitely tell that connect 202 is very happy with the 631 case here on the 202 project we start early 4:30 in the morning I mean we try to beat the heat the material that we put down it's got to hold water we got a past compaction test so when we start early we get through that much better I like the case papers good just because the comfort I mean it's quiet inside I mean totally day and night difference the ride control in there helps us out a lot and then as the traction control also for whenever we have lots of water or we're sliding a little bit it'll gear down and let you know that you know that's your sliding way too much there's no more hanging a load counter on your shoulder you can type in your name and log into that every day and it'll tell you how many tons of dirt you moved over all I'm thinking we're getting at least ten loads a day more the six thirty one case scraper it has automatic so it's a dumping assist so whenever I'm in the field I have the button pushed all I have to do is push the button go gauge the apron and to the desired height and it'll start pushing my crowd all's I have to do is keep a good rpm and I'll dump pretty flat it's more responsive in the steering as soon as you turn your turn in it vampire and connect to o2 relationship-wise has has been great connect to o2 has been a great partner to work with and I believe connect 202 is very happy with Empire and all the everything that we provided everything from service to you know just personnel just to help out with anything throughout the job [Music] [Applause] so we still have a ways to go for the connectio to project but we definitely look forward to finishing out the project with connective [Applause] [Music]"
        }
    ],
    "articulated_trucks": [
        {
        "video_id": "E2Z4xqJp5xo",
        "title": "Cat 740/745 Next Gen articulated Trucks - Assisted Hoist System (AHS) operation tutorial.",
        "url": "https://www.youtube.com/watch?v=E2Z4xqJp5xo",
        "duration": 451,
        "transcript": "well hey everybody Iron Man 3406 back here on the YouTube channel if this is your first time tuning to the channel my name's Nathan thanks for stopping by I'm going to give you guys another uh tutorial video here today on the Next Generation cat articulated trucks got a 740 GC here behind the sun it's just setting a little bit but uh 740 GC and I want to show you guys all about the assisted hoist feature that uh is in the Next Generation cat articulated trucks so I'm going to get up in the cab I'm going to put the camera on uh pause here for a second while I climb up safely and everything like that and uh yeah we'll go through this assisted hoist system with everybody it's pretty cool should make life a lot easier for truck drivers and uh yeah stay tuned thanks for watching all right everybody I am sat in the cab of this 740 GC and the switch and the feature I want to talk to you about is this guy right here so you see on the little uh in image there picture of the dump box arrows going up and down word Auto below it this is the assisted hoist system switch or AHS as caterpillar calls it this feature um defaults to off every time the key switch is turned off so if you want to use this feature you got to remember to turn it on at the start started your started your shift you'll see the little green light illuminates on the bottom of the switch telling you that it's active turn it off same deal green light goes out okay so in these next Generation CAT trucks the transmission control and the Hoist control are all built into the same same control handle here so it's nice you're not having to go from control to control to run your transmission or your gear selector and your hoist at the same time it's all nicely built into one handle with the uh um cruise control and and uh Transmission lock buttons and everything right on the on the controller but that's not what we're here to talk about we're here to talk about this assisted hoist system or the a AHS acronyms um so when we've got our automatic or our assisted hoist system uh enabled green lights on all we got to do is pull this hoist control liver past the detent let go the um service brakes are going to apply the transmission is going to be neutralized if you're in Reverse or drive and the RPMs are going to go to high idle box is going to raise when the Box gets close to the end of its hoist cycle the RPMs are going to drop a little bit so that uh saves a little a little bit of the uh stress on those cylinders instead of being at Max Force going all the way up it'll do the same thing on the way down so let's give you a little demonstration here so for the demonstration I am going to put transmission and drive we're in drive now I've got my foot on the surface brake I'm going to go ahead and give this a click so I'm going to let my foot off the brake you can see we got the transmission brakes being held RPMs went up dropped off box is all the way in the air and I'm still running my foot off the brake pedal because the brakes are applied with that AHS system when it's turned on now same thing I want to lower it I've still got my foot off the brake because the brakes are being held and the transmission being held or the brakes are applied the transmission's held I'm still in drive I'm going to go ahead and I'm going to lower my box same thing I'm going to go to the click and let go see our box starts to lower RPMs are up they drop off a little bit and box is down now even though the box is down I'm still in drive I still don't have my foot on that brake control because we're still being held until I might actually apply the service brakes put it into a different gear and then all of that turns off and I'm good to go back to get loaded and start to cycle all over again now I don't know if you can hear it or not but when that box gets almost all the way to the end the RPMs do drop a little bit so it's not so hard on those cylinders it's going to do the same thing on the way down so I'm sure you heard the RPMs drop when that box got close to the bottom just to uh save all the harsh impacts on those cylinders coming down at high idle another cool feature cat has added into these trucks is this machine stability screen now this screen is automatically going to pop up when you raise the bed um but it gives you a a sensor reading on the tractor versus the dump body so you know when you're in the green you're safe to to hoist if you get outside of that obviously not safe to uh to Hoist the body so just a nice little indicator um for you when you're when you're raising that dump body as I say it automatically pops up when you raise the bed or if you want to see it at any time while you're traveling throughout the job site you can give that button a click and it brings up that stability screen so all tied into that dump system nice visual handy to have information to keep you safe while you're hoist in the box so I hope you guys enjoyed that quick little tutorial on how to use that assisted hoist system on the new Next Generation cat articulated trucks if you find these kinds of videos useful I would appreciate a uh thumbs up like the video subscribe to the channel if you like this kind of caterpillar content I'm going to keep doing it as much as I can when time permits for you guys that are interested in the antique stuff I apologize guys I uh work's been nuts for me and I just haven't had time to work on anything so um hopefully things slow down a little bit I can get back on some of that but got to keep paying the bills and workers what pays the bills so I am going to sign off and catch you guys later thanks for watching and don't forget I am Iron Man see you next time [Music]"
        },
        {
            "video_id": "s9WS-Yp33ek",
            "title": "The Cat® 745C | Largest of the Articulated Truck Line",
            "url": "https://www.youtube.com/watch?v=s9WS-Yp33ek",
            "duration": 74,
            "transcript": "bigger payloads faster cycle times greater fuel efficiency those are just a few advantages of the new 745 see the largest of the cat articulated truck line it not only delivers 45 tons per payload it delivers more to your bottom line the 745 C comes with a new powertrain and features like the weight brake that make the truck even easier to operate it improves operator performance through advanced technologies that allow for more control over speed and braking whatever the ground conditions features like the high-density powershift transmission automatic retarder control and automatic traction control result in smoother gear changes improved acceleration and faster cycle times with that kind of expert engineering you get an articulated truck that delivers more performance more efficiency and more control at the lowest cost of production find out how much more the cat 7:45 C articulated truck can deliver to your bottom line"
        },
        {
            "video_id": "sEAaom-gqfw",
            "title": "Cat® C Series-Articulated Trucks — Principles of Operation",
            "url": "https://www.youtube.com/watch?v=sEAaom-gqfw",
            "duration": 662,
            "transcript": "The C series of articulated trucks from Caterpillar incorporates many new features which these modules aim to highlight and [Music] demonstrate. At the start of the working day, it's best practice to conduct a safety walkound inspection. The details are in your operation and maintenance manual, but the main points to cover are check for loose fittings and leaks. Check the tires for damage. Check the lights are working. Check the brakes are working. Check the fluid levels. When you're happy that your machine is in a safe condition to begin operation, deisolate the machine and make your way into the new cab. Using three points of contact, climb the steps onto the guarded walkway. If you have worked in a CAT series articulated truck, you will recognize the improvements made to the operator station. The 725 C, 730C, and 730 CEJ now have all the great operator station features from the B series and more. Make it as comfortable as possible by employing the adjustments available on the new operator's seat. Seat suspension. Inflate or deflate the airbag until the white line is in the green indicator. for and aft position. Use this handle to move the seat closer or further away and adjust to suit. Thigh support. The newly introduced thigh support helps perfect your seating position. Armrest. Finally, lower the armrest and you're ready to start your C series machine. Once the seat is in the appropriate position for you and the seat belt is fastened, you can adjust the steering wheel for tilt and reach. Check that your mirrors are positioned to give you the best visibility. If electric mirrors are fitted, the position can be changed using the switch in the cab. If this option is not fitted, the mirrors can be adjusted manually. If optional heated mirrors are fitted, activate by simply pressing this switch. As with the CAT P series articulated trucks, the color multi-purpose display or CMPD is fitted as standard to all C series machines. Now supporting up to three additional cameras and featuring an increased number of information parameters, all the information an operator needs is there at the touch of a button. Prior to starting the machine, ensure the gear selection is in neutral, the hoist lever is in the hold position, and the park brake is engaged. Start the engine, hold the brake pedal, release the park brake, and put the machine in gear. Finally, move the hoist lever into the float position. Leaving the lever in hold will limit the machine to first gear. Check the area around you is clear and pull away. The 725C retains onthe-go manual diff lock operation. When approaching a grade or poor underfoot conditions, engage the inter axle diff lock by pressing and holding the floor switch, releasing it when no longer required. For even tougher conditions, to lock up the inner and crossaxle locks, press both the floor switch and the rocker switch on the dash. The 730 CN 730 CEJ used the same automatic traction control system that was successfully introduced on the B series. Operation of the inner and cross-axxle differential locks is now fully automatic and requires no intervention from the operator. [Music] The operation of the C series retarding system remains unchanged. The three-stage system is engaged via the lever on the right hand side of the steering column. On approaching the descent of a grade, pre-select the appropriate gear and then select the correct stage of retardation. The gear selected for descending a grade should normally be the same as the gear used while ascending. Remove your foot from the throttle and cover the brake. The retarder will slow your descent and when you approach the bottom of the grade, press the throttle to disengage. The 725C retains the hydraulic retarder while the 730 C and 730 CEJ feature a new engine brake retarder. [Music] Whenever possible, position trucks at approximate right angles to the face of the bench. This gives the excavator operator an easier target. Position the truck so that the center of the body is in line with the pivot point of the hydraulic excavator. Placing the excavator on a bench above the truck will reduce the lift needed to clear the sides of the truck body. The excavator operator also has a clearer view of the truck and the area around it. The ideal height for the bench is equal to the height of the excavator stick. Ideally, the excavator should be able to load and swing 45° or less to dump the material in the truck body. The shorter the swing, the faster the loading. The loaded swing should go counterclockwise so the excavator operator has a complete view of the truck. Using a scissor tailgate will help to retain material in the truck body. Liner plates will aid in protection against damage when loading abrasive materials and rock. [Music] Select a dump area that is as firm and level as possible. This helps ensure machine stability when tipping. Minimizing maneuvering in the tip area can help reduce cycle times and fuel consumption. After coming to a stop with the machine in a straight position, tip the material using the site recommended procedure. If using an ejector, how the material is discharged can be controlled manually using the eject lever. Loads can also be dispersed on the go according to ground speed. That is, the faster you go, the thinner the spread. You can also eject loads statically as you would with a tipper machine. Material can also be ejected safely on side slopes, under overhead obstructions, when going up or down grades, and with the machine steered at an angle for access into tight spaces. In higher regulated countries to meet emissions regulations, the CAT regeneration system has been further updated and now requires the use of diesel emissions fluid or DEF. The DEF tank is filled from ground level as required. Please follow safety procedures when handling DEF fluid. When in automatic mode, regeneration is completed as the machine works without any input required by the operator. On job sites that have restrictions, regeneration can be performed manually. With the machine at operating temperature, bring it to a stop in a safe location. Select neutral. Engage the park brake. Make sure you're not pressing the throttle. Then hold down the regen switch for 5 seconds. If required, regeneration will begin. The machine can restart operation at any time during a manual regeneration. The steering lock should be used when the wheels are lifted from the ground or when an operator is working in the hitch area. The body up locking pin should be used at all times when working under the body. With the body raised, ensure the hoist lever is in the body hold position. Then fit the body prop pin. The hood raise switch is located on the dashboard. To lift or lower the hood, simply press and hold the switch. The right side cab window can be used as an emergency exit when it's not possible to leave via the cab door. The left side window in the cab door can also be used as an emergency exit by breaking the glass with the red hammer. To stop the engine, turn the key to the off position. In an emergency, the engine can be stopped from ground level. Open the service hatch. Raise the guard and move the toggle switch to the stop position. Tires should be inflated as per the manufacturer's recommendations and to suit the ground conditions. For details of maintenance intervals and scheduled servicing, please consult the operation and maintenance manual. At the end of the day, correct operation of your CS series articulated trucks make for a more efficient and profitable machine."
        },
        {
            "video_id": "pHuC3Aio87g",
            "title": "CAT 730 Articulated Dump Truck Used #fyp #cat #dumper  #dumptruck #constructionequipment #haultruck",
            "url": "https://www.youtube.com/watch?v=pHuC3Aio87g",
            "duration": 61,
            "transcript": "Here it [Music] is. So you let it go. Are you turning off your phone? [Music] And it's too far. [Music] for you. [Music] [Music] Oh sh. [Music]"
        }
    ],
    "mining_shovels": [
        {
            "video_id": "3KJWkYo88Gw",
            "title": "Cat® Hydraulic Mining Shovels",
            "url": "https://www.youtube.com/watch?v=3KJWkYo88Gw",
            "duration": 99,
            "transcript": None
        },
        {
            "video_id": "NvtFXmJ8AgU",
            "title": "Electric Rope Shovel Machines: P&H 4100 XPC, Bucyrus 495 HR, Cat 7495",
            "url": "https://www.youtube.com/watch?v=NvtFXmJ8AgU",
            "duration": 400,
            "transcript": None
        },
        {
            "video_id": "JVrrWMZ88jc",
            "title": "Cat® Mining X-2 GET",
            "url": "https://www.youtube.com/watch?v=JVrrWMZ88jc",
            "duration": 83,
            "transcript": None
        },
        {
            "video_id": "xiI-KsTGJWE",
            "title": "Experience the Cat® 6060 Hydraulic Mining Shovel",
            "url": "https://www.youtube.com/watch?v=xiI-KsTGJWE",
            "duration": 159,
            "transcript": None
        }
    ],
    "road_reclaimer": [
        {
        "video_id": "aKCw6DT2gnE",
        "title": "All-Wheel Drive | Cat® RM600/RM800 Road Reclaimers",
        "url": "https://www.youtube.com/watch?v=aKCw6DT2gnE",
        "duration": 39,
        "transcript": "[Music] the traction control system on these machines uses the same philosophy as the other cat reclaimers using four Propel pumps one for every wheel motor rather than a single Propel pump or a double Propel pump and a flow divider this system is just more efficient by measuring hydraulic pressure on each wheel the system can detect any slippage and deliver pressure more evenly to all Wheels on the machine"
        },
        {
            "video_id": "Q9J3zd3Rj8A",
            "title": "Operator Station | Cat® RM600/RM800 Road Reclaimers",
            "url": "https://www.youtube.com/watch?v=Q9J3zd3Rj8A",
            "duration": 57,
            "transcript": "[Music] the operator station rotates 90 degrees in either direction for a full 180 degrees of movement whether working from the right side or from the left side of the machine the operator can find a comfortable position for maximum visibility controls on the armrests of the operator station put everything at your fingertips and controls are grouped by function making them easy to find and easy to operate by using mini wheel steering on the left console the operator's field of view is not obstructed by a conventional steering column or console directly in front of the operator a comfortable high back heated seat comes equipped with air ride suspension for operator comfort in any condition"
        },
        {
            "video_id": "g3bVn7d0OG4",
            "title": "Joystick Controls | Cat® RM600/RM800 Road Reclaimers",
            "url": "https://www.youtube.com/watch?v=g3bVn7d0OG4",
            "duration": 124,
            "transcript": "[Music] we use a multi-function joystick on these machines for propelling the machine there's a switch on the back side of the stick that must be depressed whenever propelling forward or rearward to get the machine out of neutral that switch must be depressed and the buttons on the stick control the most commonly used rotor functions on the back of the stick we have the front rotor chamber door up and down the yellow buttons control the height of the rotor or the depth of your cut rotor up or rotor down these black buttons control the rear door of the chamber up and down in between these two buttons is a soft rubber button and this controls the rear door float function by pressing this button the rear door is put into float mode and down pressure can be adjusted on this display to apply pressure to that rear door these colored buttons on the front are the exit cut and return to cut features [Music] when the operator has the machine working at the desired depth two Taps of the green button will save that depth and it's signified by this square box around the rotor depth so when the operator reaches the end of the cut One Touch of the blue exit cut button will raise the rotor so that the operator can close the doors and fill the hole that's made at the end of the cut and one more touch of the blue button then we'll raise the machine to full transport height so the machine can be maneuvered for the next cut once in position for the next cut simply push and hold the green button and the Machine will return to the cutting depth that was previously saved"
        },
        {
            "video_id": "vLlK9xEifNU",
            "title": "Customer Testimonial: RM400 Reclaimer/Stabilizer (Texas, USA)",
            "url": "https://www.youtube.com/watch?v=vLlK9xEifNU",
            "duration": 238,
            "transcript": "Our main thing is get the tines\nin the ground and more time we\ngot them in the ground the better, better we're doing.  Cat out did themselves with\nthis, this model right here. We actually joke that the machine's smarter\nthan we are. We've had a lot\nof good luck with Caterpillar equipment, we do a lot of\nstreets, utilities, turnkey subdivision, basically.  We\nneeded a machine and chose this one. And so far it's done,\nus a good job. We're mixing a whole\nlot more material now than we used to. We were keeping a\nmachine on rent 60, 75% of the time. So we just decided to\ngo ahead and purchase one. We mainly got it\nbecause it was, you know, Cat. It moves a lot quicker. It does have more power. That's one of the things\nwe liked about it. Anytime you're mixing\nmaterial, I mean, we get paid by\nthe square yard, so the more we can mix,\nthe more we get paid. So, you know, the faster\nwe can go through it, the more money we can\nmake doing it and, you know, doing it right. We could probably\nmix 30 percent more in a day with this machine than, than we could\ngood with the, with the others. It's\nfaster and it's more accurate and that helps us all the way around. To get the proper mix. You know, you need a\nlevel ground, you know, and with the float, the longer you can keep that material\nin your drum, the better the more\nit's grinding. After we've mixed\nit the first time, then we'll put\nit on that float so it actually keeps your material in your\ndrum and then you have that uniform\nfinish at the end. The depth control\nhelps us. Once you set the\ndepth on it, you come out of a cut. You turn around and\ngo back in a cut. You just go back to\nthat same depth. It's proven to be\npretty accurate. You know, with this machine here. The blade does not have to stay with your\nmixture, you know, I can,  I'm able\nto go and do the rest of my job without having\nto baby sit the mixer. The turn radius seemed to be a\nlittle tighter. That works good\nwith Cul de sacs, with tight corners like around the radiuses\nof the roads. It works good. I like it. You can really maneuver\nthat thing to get in them tight areas.\nSpeed control, so you basically push the control forward\nand the machine's going to go as fast as it can and maintain\na certain drum speed. Man, it's, it's cut our time in\nhalf. It really has. This machine, you know,\nit has a lot of cameras on\nit that you can see, plus you can slide the cab one\nside to the other, That's a nice\nfeature for us. When you slide the cab,\nif it was static, you will have to, you know,\nextend your body. But now with the\nrotating seat you just rotate the seat, depending on which\nside the cab is, all you gotta do is\njust turn your neck a little bit and you can see where\nyou're going. The operator's\ncomfortable and he's got everything\nwithin his reach. The mixer's very big. So you really have to\nhave line of sight and able to see where\nyou're working, where you can't see you\nhave a camera so you, you know, you\nhave an extra set of eyes, the visibility\nis awesome. the cooling fan\nreverses and it helps, radiator get cleaned and\nthe AC working nice and cool. We do a lot\nof lime and cement and you can turn it, blow that stuff back out to your radiator, rather than sucking inside and clogging up\nyour radiator. This thing here has\nyour bullet teeth, the operator can easily change his teeth\nat this point, the older the\nolder machines didn't have air so you\nhad to manually beat them out with a hammer so the\noperator by himself can singlehandedly\nknock it out in no time. When we're having a\nproblem in the field. I can call my\nEquipment Manager, talk to them on the phone\nand kind of halfway diagnose something\nthat way when the mechanic\ncomes out here, he knows what he's,\nexpecting, you know, any if he needs,\nany parts or tools. He can get that on\nthe, on the way. It's a game\nchanger it really is. It's really made a\nhuge difference for us and I would\nrecommend it to anybody. I really would."
        }
    ]
}

# Summarization logic
def summarize(category):
    items = video_data.get(category, [])
    transcript = " ".join(item["transcript"] for item in items if item.get("transcript"))
    if not transcript.strip():
        return "No transcript content found for summarization."

    prompt = f"Summarize the following transcript into key points:\n\n{transcript}"
    try:
        result = model.generate_content(prompt)
        summary = result.text.strip()
        path = os.path.join(SUMMARY_DIR, f"{category}_summary.txt")
        with open(path, "w", encoding="utf-8") as f:
            f.write(summary)
        return summary
    except Exception as e:
        return f"Error: {str(e)}"

@app.route("/", methods=["GET", "POST"])
def index():
    category = request.form.get("category", "wheel_tractor")
    action = request.form.get("action", "view")
    summary = summarize(category) if action == "summarize" else None
    return render_template_string(TEMPLATE, videos=video_data[category], category=category, summary=summary)

@app.route("/download/<filename>")
def download(filename):
    path = os.path.join(SUMMARY_DIR, filename)
    return send_file(path, as_attachment=True) if os.path.exists(path) else ("Not found", 404)

# Template with full transcript shown
TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
  <title>CAT Video Summarizer</title>
  <link rel="icon" href="{{ url_for('static', filename='logo.png') }}" type="image/png">

  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-dark text-white">
<!-- Tailwind CSS (add in <head> if not already present) -->
  <script src="https://cdn.tailwindcss.com"></script>

  <!-- Replace heading and floating links with this -->
  <header class="bg-black shadow fixed top-0 left-0 w-100 z-10">
  <div class="container-fluid d-flex justify-content-between align-items-center py-3 px-4">
    <h1 class="h4 m-0 text-warning fw-bold">Learning Hub</h1>
    <div>
      <a href="/dashboard" class="btn btn-outline-warning me-2">Back to Dashboard</a>
      <a href="/logout" class="btn btn-outline-warning">Logout</a>
    </div>
  </div>
</header>
<br><br><br><br>
  <div class="container py-5">
    <h1 class="text-center text-warning mb-4">CAT Equipment Video Viewer + Transcript Summarizer</h1>

    <form method="POST" class="text-center mb-4">
      <input type="hidden" name="action" value="view">
      <div class="btn-group">
        {% for cat in ['wheel_tractor', 'articulated_trucks', 'mining_shovels', 'road_reclaimer'] %}
          <button name="category" value="{{ cat }}" class="btn btn-outline-light {% if category == cat %}active{% endif %}">{{ cat.replace('_', ' ').title() }}</button>
        {% endfor %}
      </div>
    </form>

    <div class="row g-4">
      {% for video in videos %}
        <div class="col-md-6">
          <div class="card bg-secondary text-white h-100">
            <img src="https://img.youtube.com/vi/{{ video.video_id }}/0.jpg" class="card-img-top">
            <div class="card-body">
              <h5 class="card-title">{{ video.title }}</h5>
              <p>Duration: {{ video.duration // 60 }}m {{ video.duration % 60 }}s</p>
              <a href="{{ video.url }}" target="_blank" class="btn btn-warning mb-2">Watch</a>
              {% if video.transcript %}
                <details>
                  <summary class="text-info">Show Transcript</summary>
                  <pre class="text-light bg-dark mt-2 p-2" style="max-height: 200px; overflow-y: auto;">{{ video.transcript }}</pre>
                </details>
              {% else %}
                <p class="text-muted">No transcript available.</p>
              {% endif %}
            </div>
          </div>
        </div>
      {% endfor %}
    </div>

    <form method="POST" class="mt-5 text-center">
      <input type="hidden" name="category" value="{{ category }}">
      <input type="hidden" name="action" value="summarize">
      <button class="btn btn-success">Summarize Transcripts</button>
    </form>

    {% if summary %}
    <div class="card mt-4">
      <div class="card-body bg-light text-dark">
        <h5 class="text-success">Summary:</h5>
        <pre>{{ summary }}</pre>
        <a href="/download/{{ category }}_summary.txt" class="btn btn-outline-success mt-3">Download Summary</a>
      </div>
    </div>
    {% endif %}
  </div>
</body>
</html>
"""


