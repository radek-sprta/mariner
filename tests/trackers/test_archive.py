import pytest

from mariner import torrent
from mariner.trackers import archive


class TestArchive:
    """
    Class to test Archive plugin.
    """

    def test_results(self, engine, event_loop):
        """Search returns an iterator of Torrent objects."""
        search = event_loop.run_until_complete(engine.results('plan 9'))
        search = list(search)
        assert isinstance(search[0], torrent.Torrent)
        assert len(search) == 2

    @pytest.fixture
    def engine(self, monkeypatch):
        """Return Archive instance."""
        async def mock_get(*args, **kwargs):
            return """

[Privacy Badger has replaced this AddThis button.]
The Prettifier - HTML
Enter your HTML via direct input or URL to have it formatted and syntax highlighted.

    Home
    JSON
    CSS
    JavaScript
    HTML
    SQL
    XML
    PHP
    Perl
    Apache
    Code Bin


<html>
 <head></head>
 <body>
  <div class="results" style="height: 488px;">
   <div class="item-ia mobile-header hidden-tiles hov" data-id="__mobile_header__" style="">
    <div class="views C C1">
     <span class="iconochive-eye" aria-hidden="true"></span>
     <span class="sr-only">eye</span>
    </div>
    <div class="C234">
     <div class="C C2">
      Title
     </div>
     <div class="pubdate C C3">
      <div>
       <div>
        Date Published
       </div>
      </div>
     </div>
     <div class="by C C4">
      Creator
     </div>
    </div>
    <div class="C C5"></div>
   </div>
   <div class="item-ia hov" data-id="Plan_9_from_Outer_Space_1959" data-mediatype="movies" data-year="1959" style="visibility: visible; top: 0px; left: 0px;">
    <a class="stealth" tabindex="-1" href="/details/SciFi_Horror">
     <div class="item-parent">
      <div class="item-parent-img">
       <img src="/services/img/SciFi_Horror" onerror="$(this).attr(&quot;src&quot;,&quot;/images/notfound.png&quot;)" />
      </div>
      <div class="item-parent-ttl">
       Sci-Fi / Horror
      </div>
     </div>
     <!--/.item-parent--> </a>
    <div class="hidden-tiles views C C1">
     <nobr class="hidden-xs">
      1.1
      <small>M</small>
     </nobr>
     <nobr class="hidden-sm hidden-md hidden-lg">
      1.1M
     </nobr>
    </div>
    <div class="C234">
     <div class="
              item-ttl
                                          C C2
            ">
      <a href="/details/Plan_9_from_Outer_Space_1959" title="Plan 9 from Outer Space" data-event-click-tracking="GenericNonCollection|ItemTile">
       <div class="tile-img">
        <img class="item-img " style="height:124px" src="/services/img/Plan_9_from_Outer_Space_1959" onerror="$(this).attr(&quot;src&quot;,&quot;/images/notfound.png&quot;)" />
       </div>
       <!--/.tile-img-->
       <div class="ttl">
         Plan 9 from Outer Space
       </div> </a>
     </div>
     <div class="hidden-tiles pubdate C C3">
      <nobr class="hidden-xs">
       1959
      </nobr>
      <nobr class="hidden-sm hidden-md hidden-lg">
       1959
      </nobr>
     </div>
     <div class="by C C4">
      <span class="hidden-lists">by</span>
      <span class="byv" title="Charles Burg, J. Edward Reynolds, Hugh Thomas Jr., and Edward D. Wood Jr.">Charles Burg, J. Edward Reynolds, Hugh Thomas Jr., and Edward D. Wood Jr.</span>
     </div>
     <!--/.C4-->
    </div>
    <!--/.C234-->
    <div class="statbar ">
     <div class="mt-icon C C5">
      <span class="iconochive-movies" aria-hidden="true"></span>
      <span class="sr-only">movies</span>
     </div>
     <h6 class="stat "> <span class="iconochive-eye" aria-hidden="true"></span><span class="sr-only">eye</span>
      <nobr>
       1.1
       <small>M</small>
      </nobr> </h6>
     <h6 class="stat"> <span class="iconochive-favorite" aria-hidden="true"></span><span class="sr-only">favorite</span> 262 </h6>
     <h6 class="stat"> <span class="iconochive-comment" aria-hidden="true"></span><span class="sr-only">comment</span> 38 </h6>
    </div>
    <!--/.statbar-->
   </div>
   <!--/.item-ia-->
   <div class="details-ia hidden-tiles">
    <div class="C1"></div>
    <div class="C234">
     <span>From IMDb : &quot;Can your heart stand the shocking facts about grave robbers from outer space?&quot; That's the question on the lips of the narrator of this tale about flying saucers, zombies and cardboard tombstones. A pair of aliens, angered by the &quot;stupid minds&quot; of planet Earth, set up shop in a California cemetery. Their plan: to animate an army of the dead to march on the capitals of the world. (The fact that they have only managed to resurrect three zombies to date has not...</span>
     <br />
     <span alt="4.26 out of 5 stars" title="4.26 out of 5 stars"><span class="iconochive-favorite" aria-hidden="true"></span><span class="sr-only">favorite</span><span class="iconochive-favorite" aria-hidden="true"></span><span class="sr-only">favorite</span><span class="iconochive-favorite" aria-hidden="true"></span><span class="sr-only">favorite</span><span class="iconochive-favorite" aria-hidden="true"></span><span class="sr-only">favorite</span></span> ( 38 reviews )
     <br /> Topics: Sci-Fi, Horror
     <br />
    </div>
    <div class="C5"></div>
   </div>
   <div class="item-ia hov" data-id="Plan9FromOuterSpace_811" data-mediatype="movies" data-year="1959" style="visibility: visible; top: 0px; left: 197px;">
    <a class="stealth" tabindex="-1" href="/details/SciFi_Horror">
     <div class="item-parent">
      <div class="item-parent-img">
       <img src="/services/img/SciFi_Horror" onerror="$(this).attr(&quot;src&quot;,&quot;/images/notfound.png&quot;)" />
      </div>
      <div class="item-parent-ttl">
       Sci-Fi / Horror
      </div>
     </div>
     <!--/.item-parent--> </a>
    <div class="hidden-tiles views C C1">
     <nobr class="hidden-xs">
      85,675
     </nobr>
     <nobr class="hidden-sm hidden-md hidden-lg">
      86K
     </nobr>
    </div>
    <div class="C234">
     <div class="
              item-ttl
                                          C C2
            ">
      <a href="/details/Plan9FromOuterSpace_811" title="Plan 9 from Outer Space" data-event-click-tracking="GenericNonCollection|ItemTile">
       <div class="tile-img">
        <img class="item-img " style="height:124px" src="/services/img/Plan9FromOuterSpace_811" onerror="$(this).attr(&quot;src&quot;,&quot;/images/notfound.png&quot;)" />
       </div>
       <!--/.tile-img-->
       <div class="ttl">
         Plan 9 from Outer Space
       </div> </a>
     </div>
     <div class="hidden-tiles pubdate C C3">
      <nobr class="hidden-xs">
       1959
      </nobr>
      <nobr class="hidden-sm hidden-md hidden-lg">
       1959
      </nobr>
     </div>
     <div class="by C C4">
      <span class="hidden-lists">by</span>
      <span class="byv" title="Ed Wood">Ed Wood</span>
     </div>
     <!--/.C4-->
    </div>
    <!--/.C234-->
    <div class="statbar ">
     <div class="mt-icon C C5">
      <span class="iconochive-movies" aria-hidden="true"></span>
      <span class="sr-only">movies</span>
     </div>
     <h6 class="stat "> <span class="iconochive-eye" aria-hidden="true"></span><span class="sr-only">eye</span>
      <nobr>
       85,675
      </nobr> </h6>
     <h6 class="stat"> <span class="iconochive-favorite" aria-hidden="true"></span><span class="sr-only">favorite</span> 45 </h6>
     <h6 class="stat"> <span class="iconochive-comment" aria-hidden="true"></span><span class="sr-only">comment</span> 10 </h6>
    </div>
    <!--/.statbar-->
   </div>
   <!--/.item-ia-->
   <div class="details-ia hidden-tiles">
    <div class="C1"></div>
    <div class="C234">
     <span>Aliens resurrect dead humans as zombies and vampires to stop human kind from creating the Solaranite (a sort of sun-driven bomb). - IMDB Description</span>
     <br />
     <span alt="4.60 out of 5 stars" title="4.60 out of 5 stars"><span class="iconochive-favorite" aria-hidden="true"></span><span class="sr-only">favorite</span><span class="iconochive-favorite" aria-hidden="true"></span><span class="sr-only">favorite</span><span class="iconochive-favorite" aria-hidden="true"></span><span class="sr-only">favorite</span><span class="iconochive-favorite" aria-hidden="true"></span><span class="sr-only">favorite</span><span class="iconochive-favorite" aria-hidden="true"></span><span class="sr-only">favorite</span></span> ( 10 reviews )
     <br /> Topics: Sci-Fi, Ed Wood, Movie Powder, avi, pdmovies
     <br />
    </div>
    <div class="C5"></div>
   </div>
   <div class="item-ia hov" data-id="Teenage_Zombies" data-mediatype="movies" data-year="1959" style="visibility: visible; top: 0px; left: 394px;">
    <a class="stealth" tabindex="-1" href="/details/SciFi_Horror">
     <div class="item-parent">
      <div class="item-parent-img">
       <img src="/services/img/SciFi_Horror" onerror="$(this).attr(&quot;src&quot;,&quot;/images/notfound.png&quot;)" />
      </div>
      <div class="item-parent-ttl">
       Sci-Fi / Horror
      </div>
     </div>
     <!--/.item-parent--> </a>
    <div class="hidden-tiles views C C1">
     <nobr class="hidden-xs">
      39,020
     </nobr>
     <nobr class="hidden-sm hidden-md hidden-lg">
      39K
     </nobr>
    </div>
    <div class="C234">
     <div class="
              item-ttl
                                          C C2
            ">
      <a href="/details/Teenage_Zombies" title="Teenage Zombies" data-event-click-tracking="GenericNonCollection|ItemTile">
       <div class="tile-img">
        <img class="item-img " style="height:123px" src="/services/img/Teenage_Zombies" onerror="$(this).attr(&quot;src&quot;,&quot;/images/notfound.png&quot;)" />
       </div>
       <!--/.tile-img-->
       <div class="ttl">
         Teenage Zombies
       </div> </a>
     </div>
     <div class="hidden-tiles pubdate C C3">
      <nobr class="hidden-xs">
       1959
      </nobr>
      <nobr class="hidden-sm hidden-md hidden-lg">
       1959
      </nobr>
     </div>
     <div class="by C C4">
      <span class="hidden-lists">by</span>
      <span class="byv" title="Jerry Warren">Jerry Warren</span>
     </div>
     <!--/.C4-->
    </div>
    <!--/.C234-->
    <div class="statbar ">
     <div class="mt-icon C C5">
      <span class="iconochive-movies" aria-hidden="true"></span>
      <span class="sr-only">movies</span>
     </div>
     <h6 class="stat "> <span class="iconochive-eye" aria-hidden="true"></span><span class="sr-only">eye</span>
      <nobr>
       39,020
      </nobr> </h6>
     <h6 class="stat"> <span class="iconochive-favorite" aria-hidden="true"></span><span class="sr-only">favorite</span> 36 </h6>
     <h6 class="stat"> <span class="iconochive-comment" aria-hidden="true"></span><span class="sr-only">comment</span> 10 </h6>
    </div>
    <!--/.statbar-->
   </div>
   <!--/.item-ia-->
   <div class="details-ia hidden-tiles">
    <div class="C1"></div>
    <div class="C234">
     <span>From IMDb : Teenagers Reg, Skip, Julie and Pam go out for an afternoon of water skiing on a nice day. They come ashore on an island that is being used as a testing center for a scientist and agents from &quot;an eastern power.&quot; They seek to turn the people of the United States into easily controlled zombie like creatures. The agents steal Reg's boat, stranding the teens on the island. The four friends are then held captive in cages able only to speculate on their fate. Though they have...</span>
     <br />
     <span alt="2.30 out of 5 stars" title="2.30 out of 5 stars"><span class="iconochive-favorite" aria-hidden="true"></span><span class="sr-only">favorite</span><span class="iconochive-favorite" aria-hidden="true"></span><span class="sr-only">favorite</span></span> ( 10 reviews )
     <br /> Topics: horror, pdmovies
     <br />
    </div>
    <div class="C5"></div>
   </div>
   <div class="item-ia hov" data-id="The_Bloody_Brood_movie" data-mediatype="movies" data-year="1959" style="visibility: visible; top: 0px; left: 591px;">
    <a class="stealth" tabindex="-1" href="/details/feature_films">
     <div class="item-parent">
      <div class="item-parent-img">
       <img src="/services/img/feature_films" onerror="$(this).attr(&quot;src&quot;,&quot;/images/notfound.png&quot;)" />
      </div>
      <div class="item-parent-ttl">
       Feature Films
      </div>
     </div>
     <!--/.item-parent--> </a>
    <div class="hidden-tiles views C C1">
     <nobr class="hidden-xs">
      10,332
     </nobr>
     <nobr class="hidden-sm hidden-md hidden-lg">
      10K
     </nobr>
    </div>
    <div class="C234">
     <div class="
              item-ttl
                                          C C2
            ">
      <a href="/details/The_Bloody_Brood_movie" title="The Bloody Brood" data-event-click-tracking="GenericNonCollection|ItemTile">
       <div class="tile-img">
        <img class="item-img " style="height:123px" src="/services/img/The_Bloody_Brood_movie" onerror="$(this).attr(&quot;src&quot;,&quot;/images/notfound.png&quot;)" />
       </div>
       <!--/.tile-img-->
       <div class="ttl">
         The Bloody Brood
       </div> </a>
     </div>
     <div class="hidden-tiles pubdate C C3">
      <nobr class="hidden-xs">
       1959
      </nobr>
      <nobr class="hidden-sm hidden-md hidden-lg">
       1959
      </nobr>
     </div>
     <div class="by C C4">
     </div>
     <!--/.C4-->
    </div>
    <!--/.C234-->
    <div class="statbar ">
     <div class="mt-icon C C5">
      <span class="iconochive-movies" aria-hidden="true"></span>
      <span class="sr-only">movies</span>
     </div>
     <h6 class="stat "> <span class="iconochive-eye" aria-hidden="true"></span><span class="sr-only">eye</span>
      <nobr>
       10,332
      </nobr> </h6>
     <h6 class="stat"> <span class="iconochive-favorite" aria-hidden="true"></span><span class="sr-only">favorite</span> 13 </h6>
     <h6 class="stat"> <span class="iconochive-comment" aria-hidden="true"></span><span class="sr-only">comment</span> 9 </h6>
    </div>
    <!--/.statbar-->
   </div>
   <!--/.item-ia-->
   <div class="details-ia hidden-tiles">
    <div class="C1"></div>
    <div class="C234">
     <span>Peter Falk, a drug-dealer who consorts with beatniks, decides that it would be a thrill to murder. The IMDB entry is here .</span>
     <br />
     <span alt="3.25 out of 5 stars" title="3.25 out of 5 stars"><span class="iconochive-favorite" aria-hidden="true"></span><span class="sr-only">favorite</span><span class="iconochive-favorite" aria-hidden="true"></span><span class="sr-only">favorite</span><span class="iconochive-favorite" aria-hidden="true"></span><span class="sr-only">favorite</span></span> ( 9 reviews )
     <br />
    </div>
    <div class="C5"></div>
   </div>
   <div class="item-ia hov" data-id="TeenagersFromOuterSpace" data-mediatype="movies" data-year="1959" style="visibility: visible; top: 0px; left: 788px;">
    <a class="stealth" tabindex="-1" href="/details/SciFi_Horror">
     <div class="item-parent">
      <div class="item-parent-img">
       <img src="/services/img/SciFi_Horror" onerror="$(this).attr(&quot;src&quot;,&quot;/images/notfound.png&quot;)" />
      </div>
      <div class="item-parent-ttl">
       Sci-Fi / Horror
      </div>
     </div>
     <!--/.item-parent--> </a>
    <div class="hidden-tiles views C C1">
     <nobr class="hidden-xs">
      25,412
     </nobr>
     <nobr class="hidden-sm hidden-md hidden-lg">
      25K
     </nobr>
    </div>
    <div class="C234">
     <div class="
              item-ttl
                                          C C2
            ">
      <a href="/details/TeenagersFromOuterSpace" title="Teenagers From Outer Space" data-event-click-tracking="GenericNonCollection|ItemTile">
       <div class="tile-img">
        <img class="item-img " style="height:123px" src="/services/img/TeenagersFromOuterSpace" onerror="$(this).attr(&quot;src&quot;,&quot;/images/notfound.png&quot;)" />
       </div>
       <!--/.tile-img-->
       <div class="ttl">
         Teenagers From Outer Space
       </div> </a>
     </div>
     <div class="hidden-tiles pubdate C C3">
      <nobr class="hidden-xs">
       1959
      </nobr>
      <nobr class="hidden-sm hidden-md hidden-lg">
       1959
      </nobr>
     </div>
     <div class="by C C4">
      <span class="hidden-lists">by</span>
      <span class="byv" title="Tom Graeff">Tom Graeff</span>
     </div>
     <!--/.C4-->
    </div>
    <!--/.C234-->
    <div class="statbar ">
     <div class="mt-icon C C5">
      <span class="iconochive-movies" aria-hidden="true"></span>
      <span class="sr-only">movies</span>
     </div>
     <h6 class="stat "> <span class="iconochive-eye" aria-hidden="true"></span><span class="sr-only">eye</span>
      <nobr>
       25,412
      </nobr> </h6>
     <h6 class="stat"> <span class="iconochive-favorite" aria-hidden="true"></span><span class="sr-only">favorite</span> 23 </h6>
     <h6 class="stat"> <span class="iconochive-comment" aria-hidden="true"></span><span class="sr-only">comment</span> 7 </h6>
    </div>
    <!--/.statbar-->
   </div>
   <!--/.item-ia-->
   <div class="details-ia hidden-tiles">
    <div class="C1"></div>
    <div class="C234">
     <span>A young alien (David Love) falls for a pretty teenage Earth girl (Dawn Anderson) and they team up to try to stop the plans of his invading cohorts. NOTE: This is the MPEG2 (and derivative versions). An AVI version is available here .</span>
     <br />
     <span alt="4.14 out of 5 stars" title="4.14 out of 5 stars"><span class="iconochive-favorite" aria-hidden="true"></span><span class="sr-only">favorite</span><span class="iconochive-favorite" aria-hidden="true"></span><span class="sr-only">favorite</span><span class="iconochive-favorite" aria-hidden="true"></span><span class="sr-only">favorite</span><span class="iconochive-favorite" aria-hidden="true"></span><span class="sr-only">favorite</span></span> ( 7 reviews )
     <br /> Topics: sci-fi, horror, MST3K
     <br />
    </div>
    <div class="C5"></div>
   </div>
   <div class="item-ia hov" data-id="teenagers_from_outerspace" data-mediatype="movies" data-year="1959" style="visibility: visible; top: 243px; left: 0px;">
    <a class="stealth" tabindex="-1" href="/details/SciFi_Horror">
     <div class="item-parent">
      <div class="item-parent-img">
       <img src="/services/img/SciFi_Horror" onerror="$(this).attr(&quot;src&quot;,&quot;/images/notfound.png&quot;)" />
      </div>
      <div class="item-parent-ttl">
       Sci-Fi / Horror
      </div>
     </div>
     <!--/.item-parent--> </a>
    <div class="hidden-tiles views C C1">
     <nobr class="hidden-xs">
      306,913
     </nobr>
     <nobr class="hidden-sm hidden-md hidden-lg">
      307K
     </nobr>
    </div>
    <div class="C234">
     <div class="
              item-ttl
                                          C C2
            ">
      <a href="/details/teenagers_from_outerspace" title="Teenagers from Outer Space" data-event-click-tracking="GenericNonCollection|ItemTile">
       <div class="tile-img">
        <img class="item-img " style="height:123px" src="/services/img/teenagers_from_outerspace" onerror="$(this).attr(&quot;src&quot;,&quot;/images/notfound.png&quot;)" />
       </div>
       <!--/.tile-img-->
       <div class="ttl">
         Teenagers from Outer Space
       </div> </a>
     </div>
     <div class="hidden-tiles pubdate C C3">
      <nobr class="hidden-xs">
       1959
      </nobr>
      <nobr class="hidden-sm hidden-md hidden-lg">
       1959
      </nobr>
     </div>
     <div class="by C C4">
      <span class="hidden-lists">by</span>
      <span class="byv" title="Tom Graeff">Tom Graeff</span>
     </div>
     <!--/.C4-->
    </div>
    <!--/.C234-->
    <div class="statbar ">
     <div class="mt-icon C C5">
      <span class="iconochive-movies" aria-hidden="true"></span>
      <span class="sr-only">movies</span>
     </div>
     <h6 class="stat "> <span class="iconochive-eye" aria-hidden="true"></span><span class="sr-only">eye</span>
      <nobr>
       306,913
      </nobr> </h6>
     <h6 class="stat"> <span class="iconochive-favorite" aria-hidden="true"></span><span class="sr-only">favorite</span> 81 </h6>
     <h6 class="stat"> <span class="iconochive-comment" aria-hidden="true"></span><span class="sr-only">comment</span> 22 </h6>
    </div>
    <!--/.statbar-->
   </div>
   <!--/.item-ia-->
   <div class="details-ia hidden-tiles">
    <div class="C1"></div>
    <div class="C234">
     <span>A young alien (David Love) falls for a pretty teenage Earth girl (Dawn Anderson) and they team up to try to stop the plans of his invading cohorts.</span>
     <br />
     <span alt="4.55 out of 5 stars" title="4.55 out of 5 stars"><span class="iconochive-favorite" aria-hidden="true"></span><span class="sr-only">favorite</span><span class="iconochive-favorite" aria-hidden="true"></span><span class="sr-only">favorite</span><span class="iconochive-favorite" aria-hidden="true"></span><span class="sr-only">favorite</span><span class="iconochive-favorite" aria-hidden="true"></span><span class="sr-only">favorite</span><span class="iconochive-favorite" aria-hidden="true"></span><span class="sr-only">favorite</span></span> ( 22 reviews )
     <br /> Topics: Sci-Fi, Horror
     <br />
    </div>
    <div class="C5"></div>
   </div>
  </div>
 </body>
</html>

© 2014 Josh Kristof
Contact | Change Log | Privacy Policy
            """
        monkeypatch.setattr(archive.Archive, 'get', mock_get)
        return archive.Archive()
