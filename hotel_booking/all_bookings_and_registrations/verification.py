import requests
import re

def check_hotel_on_websites(hotel_name):
    """
    Hotel එකක් Booking.com, TripAdvisor.com සහ Airbnb.com වල
    EXACTLY තියෙනවාද කියලා verify කරන function එකක්
    අවම websites 2කින් හම්බුණොත් Criteria Pass වෙනවා
    """

    url = "https://google-web-search1.p.rapidapi.com/"

    headers = {
        "x-rapidapi-key": "5cda8d51e7mshd600748ed7e4f2fp18862djsn2fc7d7a1f32f",
        "x-rapidapi-host": "google-web-search1.p.rapidapi.com"
    }

    # Check කරන්න ඕනේ websites
    websites = {
        "booking.com": False,
        "tripadvisor.com": False,
        "airbnb.com": False
    }

    print(f"\n🔍 '{hotel_name}' හොයනවා...\n")
    print("="*60)

    # එක එක website එකට search කරන්න
    for website in websites.keys():
        # Hotel නම + website නම එක්ක search query එක හදනවා
        search_query = f"{hotel_name} {website}"

        querystring = {
            "query": search_query,
            "limit": "10",
            "related_keywords": "false"
        }

        print(f"\n🔎 Search කරනවා: '{search_query}'")

        try:
            response = requests.get(url, headers=headers, params=querystring)
            data = response.json()

            # Results තියෙනවාද බලන්න
            if 'results' in data and len(data['results']) > 0:
                found = False

                # පළමු results 10 ඇතුලත බලන්න
                for i, result in enumerate(data['results'], 1):
                    result_url = result.get('url', '').lower()
                    result_title = result.get('title', '').lower()
                    result_description = result.get('description', '').lower()

                    # 1. Website එක URL එකේ තියෙනවාද check කරන්න
                    if website in result_url:
                        # 2. Hotel නම EXACTLY title එකේ හරි description එකේ තියෙනවද check කරන්න
                        hotel_name_lower = hotel_name.lower()

                        # Exact match check කරනවා (පුංචි වෙනස්කම් ignore කරමින්)
                        # Title හරි description එකේ hotel නම හරියටම තියෙනවද බලනවා
                        if hotel_name_lower in result_title or hotel_name_lower in result_description:
                            websites[website] = True
                            found = True
                            print(f"  ✅ Result #{i} එකේ හම්බුණා!")
                            print(f"     URL: {result.get('url', '')[:80]}...")
                            print(f"     Title: {result.get('title', '')[:80]}...")
                            if hotel_name_lower in result_description:
                                print(f"     Description snippet: ...{result.get('description', '')[:60]}...")
                            break

                if not found:
                    print(f"  ❌ {website} එකේ '{hotel_name}' exact නම හම්බුණේ නෑ")
            else:
                print(f"  ❌ Results හම්බුණේ නෑ")

        except Exception as e:
            print(f"  ⚠️ Error: {str(e)}")

    # කීයක් websites වල හම්බුණාද count කරන්න
    found_count = sum(websites.values())

    # Final result
    print("\n" + "="*60)
    print("\n📊 FINAL RESULT:")
    print("="*60)

    # අවම websites 2කින් හම්බුණාද check කරන්න
    if found_count >= 2:
        print("\n🎉🎉🎉 Criteria Passed 🎉🎉🎉")

        for site, status in websites.items():
            if status:
                print(f"  ✅ {site}")
            else:
                print(f"  ❌ {site} (හම්බුණේ නෑ)")

        print("\n" + "="*60)
        return True
    else:
        print("\n❌ Criteria Failed")

        found_sites = [site for site, status in websites.items() if status]
        not_found_sites = [site for site, status in websites.items() if not status]

        if found_sites:
            print("✅ හම්බුණු websites:")
            for site in found_sites:
                print(f"  • {site}")

        if not_found_sites:
            print("\n❌ හම්බුණේ නැති websites:")
            for site in not_found_sites:
                print(f"  • {site}")

        print("\n" + "="*60)
        return False