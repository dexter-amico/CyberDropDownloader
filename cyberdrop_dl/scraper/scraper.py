from __future__ import annotations

import asyncio
import re
from dataclasses import Field
from pathlib import Path
from typing import TYPE_CHECKING

import aiofiles
from yarl import URL

from cyberdrop_dl.clients.errors import NoExtensionFailure, JDownloaderFailure
from cyberdrop_dl.scraper.jdownloader import JDownloader
from cyberdrop_dl.utils.dataclasses.url_objects import ScrapeItem, MediaItem
from cyberdrop_dl.utils.utilities import log, get_filename_and_ext, get_download_path

if TYPE_CHECKING:
    from typing import List

    from cyberdrop_dl.managers.manager import Manager


class ScrapeMapper:
    """This class maps links to their respective handlers, or JDownloader if they are unsupported"""
    def __init__(self, manager: Manager):
        self.mapping = {"bunkrr": self.bunkrr, "celebforum": self.celebforum, "coomer": self.coomer,
                        "cyberdrop": self.cyberdrop, "cyberfile": self.cyberfile, "e-hentai": self.ehentai,
                        "erome": self.erome, "fapello": self.fapello, "f95zone": self.f95zone, "gofile": self.gofile,
                        "hotpic": self.hotpic, "ibb.co": self.imgbb, "imageban": self.imageban, "imgbox": self.imgbox,
                        "imgur": self.imgur, "img.kiwi": self.imgwiki, "jpg.church": self.jpgchurch,
                        "jpg.homes": self.jpgchurch, "jpg.fish": self.jpgchurch, "jpg.fishing": self.jpgchurch,
                        "jpg.pet": self.jpgchurch, "jpeg.pet": self.jpgchurch, "jpg1.su": self.jpgchurch,
                        "jpg2.su": self.jpgchurch, "jpg3.su": self.jpgchurch, "kemono": self.kemono,
                        "leakedmodels": self.leakedmodels, "mediafire": self.mediafire, "nudostar.com": self.nudostar,
                        "nudostar.tv": self.nudostartv, "omegascans": self.omegascans, "pimpandhost": self.pimpandhost,
                        "pixeldrain": self.pixeldrain, "postimg": self.postimg, "reddit": self.reddit,
                        "redd.it": self.reddit, "redgifs": self.redgifs, "rule34.xxx": self.rule34xxx,
                        "rule34.xyz": self.rule34xyz, "saint": self.saint, "scrolller": self.scrolller,
                        "simpcity": self.simpcity, "socialmediagirls": self.socialmediagirls,
                        "toonily": self.toonily, "xbunker": self.xbunker, "xbunkr": self.xbunkr}
        self.download_mapping = {"bunkrr": "bunkrr", "celebforum": "celebforum", "coomer": "coomer",
                                 "cyberdrop": "cyberdrop", "cyberfile": "cyberfile", "e-hentai": "e-hentai",
                                 "erome": "erome", "fapello": "fapello", "f95zone": "f95zone", "gofile": "gofile",
                                 "hotpic": "hotpic", "ibb.co": "imgbb", "imageban": "imageban", "imgbox": "imgbox",
                                 "imgur": "imgur", "img.kiwi": "sharex", "jpg.church": "sharex", "jpg.homes": "sharex",
                                 "jpg.fish": "sharex", "jpg.fishing": "sharex", "jpg.pet": "sharex",
                                 "jpeg.pet": "sharex", "jpg1.su": "sharex", "jpg2.su": "sharex", "jpg3.su": "sharex",
                                 "kemono": "kemono", "leakedmodels": "leakedmodels", "mediafire": "mediafire",
                                 "nudostar.com": "nudostar", "nudostar.tv": "nudostartv", "omegascans": "omegascans",
                                 "pimpandhost": "pimpandhost", "pixeldrain": "pixeldrain", "postimg": "postimg",
                                 "reddit": "reddit", "redd.it": "reddit", "redgifs": "redgifs",
                                 "rule34.xxx": "rule34.xxx", "rule34.xyz": "rule34.xyz", "saint": "saint",
                                 "scrolller": "scrolller", "simpcity": "simpcity",
                                 "socialmediagirls": "socialmediagirls",  "toonily": "toonily", "xbunker": "xbunker",
                                 "xbunkr": "xbunkr"}
        self.existing_crawlers = {}
        self.manager = manager
        self.jdownloader = JDownloader(self.manager)

        self.complete = False

    async def bunkrr(self) -> None:
        """Creates a Bunkr Crawler instance"""
        from cyberdrop_dl.scraper.crawlers.bunkrr_crawler import BunkrrCrawler
        self.existing_crawlers['bunkrr'] = BunkrrCrawler(self.manager)

    async def celebforum(self) -> None:
        """Creates a CelebForum Crawler instance"""
        from cyberdrop_dl.scraper.crawlers.celebforum_crawler import CelebForumCrawler
        self.existing_crawlers['celebforum'] = CelebForumCrawler(self.manager)

    async def coomer(self) -> None:
        """Creates a Coomer Crawler instance"""
        from cyberdrop_dl.scraper.crawlers.coomer_crawler import CoomerCrawler
        self.existing_crawlers['coomer'] = CoomerCrawler(self.manager)

    async def cyberdrop(self) -> None:
        """Creates a Cyberdrop Crawler instance"""
        from cyberdrop_dl.scraper.crawlers.cyberdrop_crawler import CyberdropCrawler
        self.existing_crawlers['cyberdrop'] = CyberdropCrawler(self.manager)

    async def cyberfile(self) -> None:
        """Creates a Cyberfile Crawler instance"""
        from cyberdrop_dl.scraper.crawlers.cyberfile_crawler import CyberfileCrawler
        self.existing_crawlers['cyberfile'] = CyberfileCrawler(self.manager)

    async def ehentai(self) -> None:
        """Creates a EHentai Crawler instance"""
        from cyberdrop_dl.scraper.crawlers.ehentai_crawler import EHentaiCrawler
        self.existing_crawlers['e-hentai'] = EHentaiCrawler(self.manager)

    async def erome(self) -> None:
        """Creates a Erome Crawler instance"""
        from cyberdrop_dl.scraper.crawlers.erome_crawler import EromeCrawler
        self.existing_crawlers['erome'] = EromeCrawler(self.manager)

    async def fapello(self) -> None:
        """Creates a Fappelo Crawler instance"""
        from cyberdrop_dl.scraper.crawlers.fapello_crawler import FapelloCrawler
        self.existing_crawlers['fapello'] = FapelloCrawler(self.manager)

    async def f95zone(self) -> None:
        """Creates a F95Zone Crawler instance"""
        from cyberdrop_dl.scraper.crawlers.f95zone_crawler import F95ZoneCrawler
        self.existing_crawlers['f95zone'] = F95ZoneCrawler(self.manager)

    async def gofile(self) -> None:
        """Creates a GoFile Crawler instance"""
        from cyberdrop_dl.scraper.crawlers.gofile_crawler import GoFileCrawler
        self.existing_crawlers['gofile'] = GoFileCrawler(self.manager)

    async def hotpic(self) -> None:
        """Creates a HotPic Crawler instance"""
        from cyberdrop_dl.scraper.crawlers.hotpic_crawler import HotPicCrawler
        self.existing_crawlers['hotpic'] = HotPicCrawler(self.manager)

    async def imageban(self) -> None:
        """Creates a ImageBan Crawler instance"""
        from cyberdrop_dl.scraper.crawlers.imageban_crawler import ImageBanCrawler
        self.existing_crawlers['imageban'] = ImageBanCrawler(self.manager)

    async def imgbb(self) -> None:
        """Creates a ImgBB Crawler instance"""
        from cyberdrop_dl.scraper.crawlers.imgbb_crawler import ImgBBCrawler
        self.existing_crawlers['ibb.co'] = ImgBBCrawler(self.manager)

    async def imgbox(self) -> None:
        """Creates a ImgBox Crawler instance"""
        from cyberdrop_dl.scraper.crawlers.imgbox_crawler import ImgBoxCrawler
        self.existing_crawlers['imgbox'] = ImgBoxCrawler(self.manager)

    async def imgur(self) -> None:
        """Creates a Imgur Crawler instance"""
        from cyberdrop_dl.scraper.crawlers.imgur_crawler import ImgurCrawler
        self.existing_crawlers['imgur'] = ImgurCrawler(self.manager)

    async def imgwiki(self) -> None:
        """Creates a ImgWiki Crawler instance"""
        from cyberdrop_dl.scraper.crawlers.imgkiwi_crawler import ImgKiwiCrawler
        self.existing_crawlers['img.kiwi'] = ImgKiwiCrawler(self.manager)

    async def jpgchurch(self) -> None:
        """Creates a JPGChurch Crawler instance"""
        from cyberdrop_dl.scraper.crawlers.jpgchurch_crawler import JPGChurchCrawler
        self.existing_crawlers['jpg.church'] = JPGChurchCrawler(self.manager)
        self.existing_crawlers['jpg.homes'] = self.existing_crawlers['jpg.church']
        self.existing_crawlers['jpg.fish'] = self.existing_crawlers['jpg.church']
        self.existing_crawlers['jpg.fishing'] = self.existing_crawlers['jpg.church']
        self.existing_crawlers['jpg.pet'] = self.existing_crawlers['jpg.church']
        self.existing_crawlers['jpeg.pet'] = self.existing_crawlers['jpg.church']
        self.existing_crawlers['jpg1.su'] = self.existing_crawlers['jpg.church']
        self.existing_crawlers['jpg2.su'] = self.existing_crawlers['jpg.church']
        self.existing_crawlers['jpg3.su'] = self.existing_crawlers['jpg.church']

    async def kemono(self) -> None:
        """Creates a Kemono Crawler instance"""
        from cyberdrop_dl.scraper.crawlers.kemono_crawler import KemonoCrawler
        self.existing_crawlers['kemono'] = KemonoCrawler(self.manager)

    async def leakedmodels(self) -> None:
        """Creates a LeakedModels Crawler instance"""
        from cyberdrop_dl.scraper.crawlers.leakedmodels_crawler import LeakedModelsCrawler
        self.existing_crawlers['leakedmodels'] = LeakedModelsCrawler(self.manager)

    async def mediafire(self) -> None:
        """Creates a MediaFire Crawler instance"""
        from cyberdrop_dl.scraper.crawlers.mediafire_crawler import MediaFireCrawler
        self.existing_crawlers['mediafire'] = MediaFireCrawler(self.manager)

    async def nudostar(self) -> None:
        """Creates a NudoStar Crawler instance"""
        from cyberdrop_dl.scraper.crawlers.nudostar_crawler import NudoStarCrawler
        self.existing_crawlers['nudostar'] = NudoStarCrawler(self.manager)

    async def nudostartv(self) -> None:
        """Creates a NudoStarTV Crawler instance"""
        from cyberdrop_dl.scraper.crawlers.nudostartv_crawler import NudoStarTVCrawler
        self.existing_crawlers['nudostar.tv'] = NudoStarTVCrawler(self.manager)

    async def omegascans(self) -> None:
        """Creates a OmegaScans Crawler instance"""
        from cyberdrop_dl.scraper.crawlers.omegascans_crawler import OmegaScansCrawler
        self.existing_crawlers['omegascans'] = OmegaScansCrawler(self.manager)

    async def pimpandhost(self) -> None:
        """Creates a PimpAndHost Crawler instance"""
        from cyberdrop_dl.scraper.crawlers.pimpandhost_crawler import PimpAndHostCrawler
        self.existing_crawlers['pimpandhost'] = PimpAndHostCrawler(self.manager)

    async def pixeldrain(self) -> None:
        """Creates a PixelDrain Crawler instance"""
        from cyberdrop_dl.scraper.crawlers.pixeldrain_crawler import PixelDrainCrawler
        self.existing_crawlers['pixeldrain'] = PixelDrainCrawler(self.manager)

    async def postimg(self) -> None:
        """Creates a PostImg Crawler instance"""
        from cyberdrop_dl.scraper.crawlers.postimg_crawler import PostImgCrawler
        self.existing_crawlers['postimg'] = PostImgCrawler(self.manager)

    async def reddit(self) -> None:
        """Creates a Reddit Crawler instance"""
        from cyberdrop_dl.scraper.crawlers.reddit_crawler import RedditCrawler
        self.existing_crawlers['reddit'] = RedditCrawler(self.manager)
        self.existing_crawlers['redd.it'] = self.existing_crawlers['reddit']

    async def redgifs(self) -> None:
        """Creates a RedGifs Crawler instance"""
        from cyberdrop_dl.scraper.crawlers.redgifs_crawler import RedGifsCrawler
        self.existing_crawlers['redgifs'] = RedGifsCrawler(self.manager)

    async def rule34xxx(self) -> None:
        """Creates a Rule34XXX Crawler instance"""
        from cyberdrop_dl.scraper.crawlers.rule34xxx_crawler import Rule34XXXCrawler
        self.existing_crawlers['rule34.xxx'] = Rule34XXXCrawler(self.manager)

    async def rule34xyz(self) -> None:
        """Creates a Rule34XYZ Crawler instance"""
        from cyberdrop_dl.scraper.crawlers.rule34xyz_crawler import Rule34XYZCrawler
        self.existing_crawlers['rule34.xyz'] = Rule34XYZCrawler(self.manager)

    async def saint(self) -> None:
        """Creates a Saint Crawler instance"""
        from cyberdrop_dl.scraper.crawlers.saint_crawler import SaintCrawler
        self.existing_crawlers['saint'] = SaintCrawler(self.manager)

    async def scrolller(self) -> None:
        """Creates a Scrolller Crawler instance"""
        from cyberdrop_dl.scraper.crawlers.scrolller_crawler import ScrolllerCrawler
        self.existing_crawlers['scrolller'] = ScrolllerCrawler(self.manager)

    async def simpcity(self) -> None:
        """Creates a SimpCity Crawler instance"""
        from cyberdrop_dl.scraper.crawlers.simpcity_crawler import SimpCityCrawler
        self.existing_crawlers['simpcity'] = SimpCityCrawler(self.manager)

    async def socialmediagirls(self) -> None:
        """Creates a SocialMediaGirls Crawler instance"""
        from cyberdrop_dl.scraper.crawlers.socialmediagirls_crawler import SocialMediaGirlsCrawler
        self.existing_crawlers['socialmediagirls'] = SocialMediaGirlsCrawler(self.manager)

    async def toonily(self) -> None:
        """Creates a Toonily Crawler instance"""
        from cyberdrop_dl.scraper.crawlers.toonily_crawler import ToonilyCrawler
        self.existing_crawlers['toonily'] = ToonilyCrawler(self.manager)

    async def xbunker(self) -> None:
        """Creates a XBunker Crawler instance"""
        from cyberdrop_dl.scraper.crawlers.xbunker_crawler import XBunkerCrawler
        self.existing_crawlers['xbunker'] = XBunkerCrawler(self.manager)

    async def xbunkr(self) -> None:
        """Creates a XBunkr Crawler instance"""
        from cyberdrop_dl.scraper.crawlers.xbunkr_crawler import XBunkrCrawler
        self.existing_crawlers['xbunkr'] = XBunkrCrawler(self.manager)

    """~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""

    async def regex_links(self, line: str) -> List:
        """Regex grab the links from the URLs.txt file
        This allows code blocks or full paragraphs to be copy and pasted into the URLs.txt"""
        yarl_links = []
        if line.lstrip().rstrip().startswith('#'):
            return yarl_links

        all_links = [x.group().replace(".md.", ".") for x in re.finditer(
            r"(?:http.*?)(?=($|\n|\r\n|\r|\s|\"|\[/URL]|']\[|]\[|\[/img]))", line)]
        for link in all_links:
            yarl_links.append(URL(link))
        return yarl_links

    async def load_links(self) -> None:
        """Loads links from args / input file"""
        links = []
        async with aiofiles.open(self.manager.path_manager.input_file, "r", encoding="utf8") as f:
            async for line in f:
                assert isinstance(line, str)
                links.extend(await self.regex_links(line))
        links.extend(self.manager.args_manager.other_links)
        links = list(filter(None, links))

        if not links:
            await log("No valid links found.")
        for link in links:
            item = ScrapeItem(url=link, parent_title="")
            await self.manager.queue_manager.url_objects_to_map.put(item)

    async def load_failed_links(self) -> None:
        """Loads failed links from db"""
        items = await self.manager.db_manager.history_table.get_failed_items()
        for item in items:
            link = URL(item[2])
            retry_path = Path(item[3])

            item = ScrapeItem(link, parent_title="", part_of_album=True, retry=True, retry_path=retry_path)
            await self.manager.queue_manager.url_objects_to_map.put(item)

    async def extension_check(self, url: URL) -> bool:
        """Checks if the URL has a valid extension"""
        try:
            filename, ext = await get_filename_and_ext(url.name)

            from cyberdrop_dl.utils.utilities import FILE_FORMATS
            if ext in FILE_FORMATS['Images'] or ext in FILE_FORMATS['Videos'] or ext in FILE_FORMATS['Audio']:
                return True
            return False
        except NoExtensionFailure:
            return False

    """~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""

    async def check_complete(self) -> bool:
        if self.manager.queue_manager.url_objects_to_map.empty():
            for crawler in self.existing_crawlers.values():
                if not crawler.complete:
                    return False
            return True
        return False

    async def map_urls(self) -> None:
        """Maps URLs to their respective handlers"""
        while True:
            self.complete = False
            scrape_item: ScrapeItem = await self.manager.queue_manager.url_objects_to_map.get()

            if not scrape_item.url:
                continue
            if not isinstance(scrape_item.url, URL):
                try:
                    scrape_item.url = URL(scrape_item.url)
                except Exception as e:
                    continue

            try:
                if not scrape_item.url.host:
                    continue
            except Exception as e:
                continue

            skip = False
            for skip_host in self.manager.config_manager.settings_data['Ignore_Options']['skip_hosts']:
                if skip_host in scrape_item.url.host:
                    skip = True
                    break
            for only_host in self.manager.config_manager.settings_data['Ignore_Options']['only_hosts']:
                if only_host not in scrape_item.url.host:
                    skip = True
                    break

            if str(scrape_item.url).endswith("/"):
                if scrape_item.url.query_string:
                    query = scrape_item.url.query_string[:-1]
                    scrape_item.url = scrape_item.url.with_query(query)
                else:
                    scrape_item.url = scrape_item.url.with_path(scrape_item.url.path[:-1])

            key = next((key for key in self.mapping if key in scrape_item.url.host.lower()), None)
            download_key = next((self.download_mapping[key] for key in self.download_mapping if key in scrape_item.url.host.lower()), None)

            if key and not skip:
                """If the crawler doesn't exist, create it, finally add the scrape item to it's queue"""
                if not self.existing_crawlers.get(key):
                    start_handler = self.mapping[key]
                    await start_handler()
                    await self.existing_crawlers[key].startup()
                    await self.manager.download_manager.get_download_instance(download_key)
                    asyncio.create_task(self.existing_crawlers[key].run_loop())
                await self.existing_crawlers[key].scraper_queue.put(scrape_item)
                await asyncio.sleep(0)
                continue
            elif skip:
                await log(f"Skipping URL by Config Selections: {scrape_item.url}")
            elif await self.extension_check(scrape_item.url):
                await self.manager.download_manager.get_download_instance("no_crawler")
                check_complete = await self.manager.db_manager.history_table.check_complete("no_crawler", scrape_item.url)
                if check_complete:
                    await log(f"Skipping {scrape_item.url} as it has already been downloaded")
                    await self.manager.progress_manager.download_progress.add_previously_completed()
                    continue
                download_queue = await self.manager.queue_manager.get_download_queue("no_crawler")
                await scrape_item.add_to_parent_title("Loose Files")
                scrape_item.part_of_album = True
                download_folder = await get_download_path(self.manager, scrape_item, "no_crawler")
                filename, ext = await get_filename_and_ext(scrape_item.url.name)
                media_item = MediaItem(scrape_item.url, scrape_item.url, download_folder, filename, ext, filename)
                await download_queue.put(media_item)
            elif self.jdownloader.enabled:
                if isinstance(self.jdownloader.jdownloader_agent, Field):
                    await self.jdownloader.jdownloader_setup()
                    if not self.jdownloader.enabled:
                        await log(f"Unsupported URL: {scrape_item.url}")
                        await self.manager.log_manager.write_unsupported_urls_log(scrape_item.url)
                await log(f"Sending unsupported URL to JDownloader: {scrape_item.url}")
                try:
                    await self.jdownloader.direct_unsupported_to_jdownloader(scrape_item.url, scrape_item.parent_title)
                except JDownloaderFailure as e:
                    await log(f"Failed to send {scrape_item.url} to JDownloader")
                    await log(e.message)
                    await self.manager.log_manager.write_unsupported_urls_log(scrape_item.url)
            else:
                await log(f"Unsupported URL: {scrape_item.url}")
                await self.manager.log_manager.write_unsupported_urls_log(scrape_item.url)

            if self.complete:
                break