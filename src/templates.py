"""
Theme instructions and fallback HTML templates.
"""

from typing import Dict, Optional


def get_theme_instructions(theme: str) -> str:
    """Return detailed design directives for the chosen theme."""

    if theme == "light":
        return """
**Theme Goal: Light & Professional**

Generate a design that feels **bright, energetic, and modern** with sophisticated visual depth.

- **Color Palette:** Embrace a vibrant spectrum with soft pastels, warm whites, and bright accent colors. Use gradient backgrounds transitioning from light blues to soft purples, or warm peachy tones to cream. Incorporate multiple complementary colors rather than monochrome approaches.

- **Background Effects:** Implement subtle geometric patterns, soft diagonal gradients, gentle wave patterns, or abstract shape overlays. Consider light particle effects, floating elements, or animated background patterns that add movement without overwhelming content.

- **Visual Elements:** Apply soft drop shadows with multiple layers, gentle blur effects for depth, rounded corners with varying radii, and subtle border gradients. Use glassmorphism effects with semi-transparent elements and backdrop filters.

- **Interactive Effects:** Incorporate smooth hover animations, color transitions on interaction, gentle bounce effects, and progressive loading animations. Add micro-interactions like button transformations and content reveal animations.

- **Typography & Spacing:** Use varied font weights and sizes to create hierarchy, generous whitespace with rhythmic spacing patterns, and text effects like subtle shadows or gradient fills for headings.
"""

    elif theme == "dark":
        return """
**Theme Goal: Dark & Immersive**

Generate a design that is **dramatic, sophisticated, and cutting-edge** with rich visual complexity.

- **Color Palette:** Utilize deep, rich color combinations with electric accents. Blend dark purples with neon blues, charcoal grays with vibrant magentas, or midnight blues with golden highlights. Embrace high-contrast color relationships and metallic undertones.

- **Background Effects:** Create dynamic dark gradients with multiple color stops, abstract dark patterns with glowing elements, constellation-like dot patterns, or digital grid overlays. Implement subtle animated elements like floating particles, pulsing glows, or shifting gradient animations.

- **Visual Elements:** Apply glowing box shadows, neon-style border effects, elevated card designs with strong shadows, and light emission effects. Use dark glassmorphism with glowing edges, metallic gradients, and holographic accent details.

- **Interactive Effects:** Incorporate glowing hover states, electric pulse animations, smooth color morphing transitions, and dramatic scale transformations. Add cyberpunk-inspired effects like digital glitch animations and neon trail effects.

- **Typography & Spacing:** Implement dramatic contrast with bold headlines, subtle text glows for enhanced readability, and dynamic spacing that creates visual tension and release patterns.
"""

    else:
        return """
**Theme Goal: Sophisticated & Balanced**

Generate a design that is **refined, trustworthy, and elegantly modern** with subtle premium touches.

- **Color Palette:** Employ sophisticated neutral combinations with strategic accent colors. Blend warm grays with sage greens, beiges with terracotta accents, or cool grays with navy blues. Use earthtone gradients and muted color harmonies that convey stability and premium quality.

- **Background Effects:** Create subtle texture overlays, gentle linear gradients at 45-degree angles, organic shape patterns, or minimalist geometric designs. Implement paper-like textures, subtle noise patterns, or soft architectural-inspired backgrounds.

- **Visual Elements:** Apply refined shadow systems with multiple depth layers, elegant border treatments with subtle color variations, premium card designs with sophisticated elevation, and tasteful accent lines or dividers.

- **Interactive Effects:** Incorporate smooth, professional animations, gentle scale transitions, elegant fade effects, and refined hover states. Add sophisticated micro-interactions like progressive reveals and smooth parallax scrolling effects.

- **Typography & Spacing:** Use premium typography hierarchies, balanced whitespace that breathes, subtle text treatments that enhance readability, and classical proportions that convey authority and trustworthiness.
"""


def create_fallback_html(
    business_info: Dict,
    theme: str,
    sections: Dict,
    hero_image_url: Optional[str],
) -> str:
    """Generate a minimal but functional HTML page when integration fails."""

    name = business_info.get("business_name", "Your Business")
    btype = business_info.get("business_type", "Business")

    bg = "bg-gray-900 text-white" if theme == "dark" else "bg-white text-gray-900"
    nav_bg = "bg-gray-800" if theme == "dark" else "bg-blue-600"
    hero_bg = (
        "bg-gradient-to-r from-gray-900 to-blue-900"
        if theme == "dark"
        else "bg-gradient-to-r from-blue-600 to-purple-600"
    )
    footer_bg = "bg-gray-800" if theme == "dark" else "bg-gray-900"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name} — {btype} Solutions</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.css" rel="stylesheet">
</head>
<body class="{bg}">
    <nav class="p-4 {nav_bg}">
        <div class="container mx-auto flex justify-between items-center">
            <h1 class="text-2xl font-bold text-white">{name}</h1>
            <div class="space-x-4">
                <a href="#services" class="text-white hover:text-blue-200">Services</a>
                <a href="#about" class="text-white hover:text-blue-200">About</a>
                <a href="#contact" class="text-white hover:text-blue-200">Contact</a>
            </div>
        </div>
    </nav>

    <section class="py-20 {hero_bg} text-white">
        <div class="container mx-auto text-center">
            <h1 class="text-5xl font-bold mb-6">Professional {btype} Solutions</h1>
            <p class="text-xl mb-8">Delivering excellence in {btype.lower()} services</p>
            <button class="bg-white text-blue-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100">Get Started</button>
        </div>
    </section>

    <section id="services" class="py-16">
        <div class="container mx-auto">
            <h2 class="text-3xl font-bold text-center mb-12">Our Services</h2>
            <div class="grid md:grid-cols-3 gap-8 px-4">
                <div class="text-center p-6 rounded-lg shadow-lg">
                    <i class="bi bi-star text-4xl text-blue-600 mb-4"></i>
                    <h3 class="text-xl font-semibold mb-2">Quality Service</h3>
                    <p>Professional {btype.lower()} solutions tailored to your needs.</p>
                </div>
                <div class="text-center p-6 rounded-lg shadow-lg">
                    <i class="bi bi-people text-4xl text-blue-600 mb-4"></i>
                    <h3 class="text-xl font-semibold mb-2">Expert Team</h3>
                    <p>Experienced professionals dedicated to your success.</p>
                </div>
                <div class="text-center p-6 rounded-lg shadow-lg">
                    <i class="bi bi-trophy text-4xl text-blue-600 mb-4"></i>
                    <h3 class="text-xl font-semibold mb-2">Proven Results</h3>
                    <p>Track record of delivering exceptional outcomes.</p>
                </div>
            </div>
        </div>
    </section>

    <footer class="{footer_bg} text-white py-8">
        <div class="container mx-auto text-center">
            <p>&copy; 2026 {name}. All rights reserved.</p>
            <div class="mt-4 space-x-4">
                <a href="#" class="text-blue-400 hover:text-blue-300"><i class="bi bi-facebook"></i></a>
                <a href="#" class="text-blue-400 hover:text-blue-300"><i class="bi bi-twitter-x"></i></a>
                <a href="#" class="text-blue-400 hover:text-blue-300"><i class="bi bi-linkedin"></i></a>
            </div>
        </div>
    </footer>
</body>
</html>"""
