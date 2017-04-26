from urllib.parse import urlparse

from sdalg.sd_algorithm import SDAlgorithm

URLS_TO_PARSE = ["http://acara.co.id/event/jakarta-kids-dash-2016/",
                 "http://prague.eventful.com/events/system-down-/E0-001-097094935-1",
                 "https://www.eventbrite.com/e/christmas-dataparty-tickets-30043454782?aff=ehomecard",
                 "https://www.meetup.com/Prague-Radical-Honesty-Group/events/235332136/",
                 "http://www.last.fm/event/4278840+Marissa+Nadler+at+MeetFactory+on+14+December+2016",
                 "https://kudago.com/spb/event/noch-pozhiratelej/",
                 "http://www.eventfinda.co.nz/2016/russian-level-beginners-course8/auckland/parnell",
                 "http://www.eventim.co.uk/emeli-sande-Tickets.html?affiliate=EUK&doc=artistPages%2Ftickets&fun=artist&action=tickets&erid=1798300",
                 "http://www.sfstation.com/the-emerald-cup-the-academy-awards-of-the-cannabis-industry-e2305199",
                 "http://www.timeout.com/barcelona/music/sidecar-5-000-concerts-nick-lowe-los-straitjackets",
                 "https://www.expats.cz/prague/entertainment/37855-15-let-zrni-vol-1-specialni-host-porok-karpo-tibet-ch.html",
                 "http://www.prague.eu/en/event/10025/aida?back=1",
                 "https://www.pragueeventscalendar.cz/cs-cz/events/detail/260496/royal-russian-ballet",
                 "https://www.pragueeventscalendar.com/en-gb/events/detail/261867/the-best-of-swan-lake-pitchaikovsky",
                 "https://www.pragueticketoffice.com/event/1109899-advent-christmas-concert-great-organ-music/2016-12-12-17-00/"]

sd = SDAlgorithm()

for url in URLS_TO_PARSE:
    sd.url = url
    parced_url = urlparse(url=url)
    domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parced_url)
    print("\n \n ========={}========== \n \n".format(domain))
    sd.analyze_page()
    try:
        pass
    except IndexError:
        pass
    finally:
        print("\n \n ERROR WHILE PROCESSING! \n \n")
