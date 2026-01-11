export default {
  async fetch(request, env, ctx) {
    try {
      const nzUrl = "https://raw.githubusercontent.com/cricstreamz745/Web-Iptv/refs/heads/main/nz.json";

      const nzRes = await fetch(nzUrl);
      const nz = await nzRes.json();

      let output = [];

      for (const item of nz.channels) {
        let mpdText = "";

        try {
          const mpdRes = await fetch(item.fetch_url, {
            headers: {
              "Referer": "https://webiptv.site/",
              "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
              "Accept": "*/*",
              "Accept-Language": "en-US,en;q=0.9",
              "Origin": "https://webiptv.site",
              "Connection": "keep-alive",
              "Sec-Fetch-Dest": "empty",
              "Sec-Fetch-Mode": "cors",
              "Sec-Fetch-Site": "same-site",
              "Pragma": "no-cache",
              "Cache-Control": "no-cache"
            }
          });

          mpdText = await mpdRes.text();
        } catch (e) {
          continue;
        }

        // Only keep REAL MPD
        if (!mpdText.includes("<MPD")) {
          continue;
        }

        output.push({
          name: item.name,
          thumb: item.thumb,
          mpd: mpdText,
          kid: item.kid,
          key: item.key
        });
      }

      return new Response(JSON.stringify(output, null, 2), {
        headers: {
          "content-type": "application/json",
          "access-control-allow-origin": "*"
        }
      });

    } catch (err) {
      return new Response(
        JSON.stringify({ error: err.message }),
        { status: 500, headers: { "content-type": "application/json" } }
      );
    }
  }
};
