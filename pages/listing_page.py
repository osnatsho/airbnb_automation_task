from pages.base_page import BasePage

class ListingPage(BasePage):
    async def get_reservation_summary(self):
        await self.wait_for_selector('[data-testid="BookIt-default"]')
        title = await self.page.locator("h1").text_content()
        total_price = await self.page.locator('[data-testid="PriceSection"]').text_content()
        return {
            "title": title.strip() if title else "N/A",
            "total_price": total_price.strip() if total_price else "N/A"
        }

    async def click_reserve(self):
        await self.page.locator("button", has_text="Reserve").click()

    async def enter_phone_number(self, phone_number: str):
        try:
            await self.page.locator('input[type="tel"]').fill(phone_number)
        except:
            pass  # if no phone field is available, ignore

    async def verify_family_suitability(self):
        """Verify that the listing is suitable for a family with children."""
        # Check if amenities section is available
        amenities_section = await self.page.query_selector('[data-section-id="AMENITIES_DEFAULT"]')
        
        if amenities_section:
            amenities_text = await amenities_section.text_content()
            
            # Check for family-friendly amenities
            family_amenities = [
                "crib", "high chair", "children's books", "children's toys", 
                "family friendly", "children's dinnerware", "babysitter", 
                "baby bath", "children's games", "playground"
            ]
            
            found_amenities = []
            for amenity in family_amenities:
                if amenity.lower() in amenities_text.lower():
                    found_amenities.append(amenity)
            
            return {
                "is_family_suitable": len(found_amenities) > 0,
                "family_amenities": found_amenities
            }
        
        # If listing mentions "family" or "children" in the title or description
        title = await self.page.locator("h1").text_content()
        description = await self.page.locator('[data-section-id="DESCRIPTION_DEFAULT"]').text_content()
        combined_text = (title + " " + description).lower()
        
        has_family_keywords = any(keyword in combined_text for keyword in [
            "family", "child", "children", "kid", "kids", "baby", "infant"
        ])
        
        return {
            "is_family_suitable": has_family_keywords,
            "family_amenities": []
        }

    async def check_accommodation_limits(self):
        """Check the maximum number of guests and if children are welcome."""
        try:
            # Look for the section showing guest limits
            guest_info = await self.page.locator('[data-testid="guest-details-guest-count"]').text_content()
            
            # Check if the listing mentions it's suitable for children
            rules_section = await self.page.locator('[data-section-id="house-rules-panel"]').text_content()
            children_allowed = "not suitable for children" not in rules_section.lower()
            
            return {
                "guest_info": guest_info.strip() if guest_info else "N/A",
                "children_allowed": children_allowed
            }
        except Exception as e:
            print(f"Error checking accommodation limits: {e}")
            return {
                "guest_info": "Information not found",
                "children_allowed": True  # Default to true if we can't find explicit info
            }