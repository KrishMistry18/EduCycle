import re
import random
from datetime import datetime
from .models import ChatMessage, Item, User, Order

class EduCycleChatbot:
    def __init__(self):
        self.greetings = ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening', 'greetings']
        self.farewells = ['bye', 'goodbye', 'see you', 'thanks', 'thank you', 'exit', 'quit']
        self.help_keywords = ['help', 'guide', 'how', 'what', 'where', 'when', 'why', 'assist']
        
        # Enhanced conversation flows with more comprehensive responses
        self.conversation_flows = {
            'greeting': {
                'patterns': self.greetings,
                'responses': [
                    "Hello! Welcome to EduCycle! I'm your AI assistant here to help you navigate our student marketplace. How can I assist you today?",
                    "Hi there! I'm your EduCycle assistant. I can help you with buying, selling, account management, safety guidelines, and more. What would you like to know?",
                    "Hey! Welcome to EduCycle! I'm here to guide you through our student marketplace. What can I help you with today?"
                ]
            },
            'farewell': {
                'patterns': self.farewells,
                'responses': [
                    "You're welcome! Feel free to come back if you need more help. Happy trading on EduCycle!",
                    "Goodbye! Have a great day and happy shopping/selling on EduCycle!",
                    "Thanks for chatting! Don't hesitate to ask if you need help later. See you around!"
                ]
            },
            'buying': {
                'patterns': ['buy', 'purchase', 'shop', 'buying', 'how to buy', 'buy item', 'order', 'checkout', 'cart', 'buying items', 'how do i buy', 'purchase items'],
                'responses': [
                    "🛒 **How to Buy on EduCycle:**\n\n1. **Browse Items**: Visit the homepage or search for specific items\n2. **View Details**: Click on any item to see full description, photos, and seller info\n3. **Add to Cart**: Click 'Add to Cart' or contact seller directly\n4. **Checkout**: Complete your purchase through our secure checkout\n5. **Arrange Pickup**: Coordinate with seller for pickup/delivery\n\n💡 **Tips**: Always read item descriptions carefully and ask sellers questions before buying!",
                    
                    "📦 **Buying Process:**\n\n• Browse our item listings on the homepage\n• Use search filters to find specific items\n• Click on items to view detailed information\n• Add items to your cart or message sellers\n• Complete secure checkout process\n• Arrange pickup/delivery with seller\n\n🔍 **Pro Tip**: You can message sellers to ask questions before purchasing!",
                    
                    "🛍️ **Shopping Guide:**\n\n1. **Search & Browse**: Find items using search or category filters\n2. **Item Details**: Check photos, descriptions, and seller ratings\n3. **Contact Seller**: Message sellers for more information\n4. **Purchase**: Add to cart and complete checkout\n5. **Pickup**: Meet seller in safe, public location\n\n✅ **Safety**: Always meet in public places and verify items before paying!"
                ]
            },
            'selling': {
                'patterns': ['sell', 'selling', 'list', 'add item', 'post item', 'how to sell', 'create listing', 'upload item', 'selling items', 'how do i sell', 'list item'],
                'responses': [
                    "💰 **Complete Selling Guide:**\n\n**Step 1: Prepare Your Item**\n• Clean and organize your item\n• Take high-quality photos (good lighting, multiple angles)\n• Research similar items and their prices\n• Determine fair market value\n\n**Step 2: Create Listing**\n• Login to your EduCycle account\n• Click 'Sell' or 'Add Item' button\n• Fill in detailed description (condition, features, why selling)\n• Upload 3-5 clear photos\n• Set competitive price\n• Choose correct category\n\n**Step 3: Optimize for Sales**\n• Write compelling title with key details\n• Include all relevant information (size, brand, condition)\n• Mention any defects honestly\n• Add why you're selling (upgrading, moving, etc.)\n• Set reasonable price (check similar items)\n\n**Step 4: Manage Inquiries**\n• Respond to messages within 24 hours\n• Answer all questions thoroughly\n• Be honest about item condition\n• Negotiate fairly but know your bottom line\n• Provide additional photos if requested\n\n**Step 5: Complete Sale**\n• Agree on meeting time and location\n• Choose safe, public meeting spot\n• Verify payment before handing over item\n• Keep all communication records\n\n💡 **Pro Tips:**\n• Good photos sell 3x faster\n• Respond quickly to increase sales\n• Honest descriptions build trust\n• Competitive pricing attracts buyers",
                    
                    "📝 **Smart Selling Strategy:**\n\n**Before Listing:**\n• Research what similar items sell for\n• Take professional-quality photos\n• Write detailed, honest descriptions\n• Set realistic expectations\n\n**During Sale:**\n• Respond to messages promptly\n• Be transparent about item condition\n• Provide additional information when asked\n• Negotiate fairly but don't undervalue\n\n**After Sale:**\n• Meet in safe, public locations\n• Verify payment before exchange\n• Leave honest reviews for buyers\n• Build reputation for future sales\n\n✅ **Success Formula:** Great photos + honest descriptions + quick responses = faster sales!",
                    
                    "🛒 **Selling Best Practices:**\n\n**Creating Great Listings:**\n• Use natural lighting for photos\n• Show item from multiple angles\n• Include close-ups of any defects\n• Write detailed, honest descriptions\n• Mention brand, model, and condition\n\n**Pricing Strategy:**\n• Research similar items on platform\n• Consider original purchase price\n• Factor in wear and tear\n• Start competitive, adjust if needed\n• Be open to reasonable offers\n\n**Customer Service:**\n• Respond to messages within hours\n• Answer all questions thoroughly\n• Provide additional photos if needed\n• Be honest about any issues\n• Maintain professional communication\n\n**Safe Transactions:**\n• Meet in campus libraries or cafes\n• Verify payment before exchange\n• Keep all communication records\n• Trust your instincts\n\n🎯 **Goal**: Build reputation for honest, reliable selling!"
                ]
            },
            'account': {
                'patterns': ['account', 'profile', 'register', 'sign up', 'login', 'sign in', 'create account', 'user account'],
                'responses': [
                    "👤 **Complete Account Guide:**\n\n**Creating Your Account:**\n1. **Click 'Sign Up'** in the top navigation\n2. **Fill in Details**:\n   • Full name (as it appears on your ID)\n   • Student email address (required)\n   • Strong password (8+ characters)\n   • Phone number (optional but recommended)\n3. **Student Information**:\n   • Department/Major\n   • Year of study\n   • Student ID (optional)\n   • Campus location\n4. **Verify Email**: Check your inbox and click verification link\n5. **Complete Profile**: Add profile picture and additional details\n6. **Start Using**: Begin buying and selling!\n\n**Login Process:**\n• Use your email address or username\n• Enter your password\n• Enable 'Remember Me' for convenience\n• Use 'Forgot Password' if needed\n\n**Profile Management:**\n• Update personal information anytime\n• Add/change profile picture\n• Manage notification preferences\n• Update contact details\n• Set privacy settings\n\n💡 **Pro Tips:**\n• Use your student email for verification\n• Choose a strong, unique password\n• Keep your contact info updated\n• Add a profile picture for trust",
                    
                    "📝 **Account Setup & Management:**\n\n**Registration Steps:**\n• Click 'Sign Up' button in navigation\n• Enter accurate student details\n• Use your official student email\n• Create a strong password\n• Verify your email address\n• Complete your profile setup\n\n**Login Options:**\n• Use email address or username\n• Enter your password\n• Enable 'Remember Me' for convenience\n• Use 'Forgot Password' if locked out\n\n**Profile Customization:**\n• Update contact information\n• Add student ID for verification\n• Set your department and year\n• Manage privacy and notification settings\n• Add profile picture for credibility\n• Update location preferences\n\n**Account Security:**\n• Use strong, unique passwords\n• Enable two-factor authentication if available\n• Keep contact information updated\n• Regularly check account activity\n• Report suspicious activity immediately\n\n✅ **Your account is your identity on EduCycle!**",
                    
                    "🔐 **Account Help & Troubleshooting:**\n\n**For New Users:**\n1. **Click 'Sign Up'** to create your account\n2. **Use Student Email**: Your official university email address\n3. **Add Student Details**: Department, year, and student ID\n4. **Verify Email**: Check inbox and click verification link\n5. **Complete Profile**: Add photo and additional information\n6. **Start Trading**: Begin buying and selling items!\n\n**For Existing Users:**\n• **Login**: Use email/username and password\n• **Password Reset**: Click 'Forgot Password' if needed\n• **Profile Updates**: Keep information current\n• **Account Settings**: Manage preferences and privacy\n• **Security**: Monitor account activity\n\n**Common Issues:**\n• **Can't Login**: Check email/username spelling\n• **Password Issues**: Use 'Forgot Password' link\n• **Email Not Verified**: Check spam folder\n• **Profile Problems**: Contact support for help\n\n**Account Benefits:**\n• Track your buying and selling history\n• Manage your listings and messages\n• Build reputation and reviews\n• Access platform features\n• Get notifications about your items\n\n🎯 **Your account is your gateway to the EduCycle community!**"
                ]
            },
            'safety': {
                'patterns': ['safe', 'safety', 'secure', 'trust', 'meet', 'pickup', 'delivery', 'scam', 'fraud', 'danger', 'is it safe', 'meeting safely', 'safe to meet'],
                'responses': [
                    "🛡️ **Complete Safety Guide:**\n\n**Safe Meeting Locations:**\n• Campus libraries (most recommended)\n• Student centers and common areas\n• Public cafes and restaurants\n• Shopping centers and malls\n• Well-lit, populated areas\n\n**Meeting Best Practices:**\n• Always meet in public places\n• Bring a friend if possible\n• Meet during daylight hours\n• Tell someone where you're going\n• Trust your instincts\n\n**Payment Safety:**\n• Verify item condition before paying\n• Use cash or secure digital payments\n• Avoid sharing personal financial info\n• Keep all transaction records\n• Don't pay before seeing the item\n\n**Red Flags to Watch For:**\n• Pressure to meet in isolated areas\n• Requests for personal financial information\n• Suspicious payment methods\n• Aggressive or threatening behavior\n• Items that seem too good to be true\n\n**If Something Goes Wrong:**\n• Leave immediately if you feel unsafe\n• Report suspicious activity to support\n• Block problematic users\n• Contact campus security if needed\n• Keep all communication records\n\n✅ **Your safety is our top priority!**",
                    
                    "🔒 **Security Best Practices:**\n\n**Before Meeting:**\n• Research the other person's profile\n• Check their ratings and reviews\n• Communicate clearly about meeting details\n• Agree on payment method beforehand\n• Choose a safe, public location\n\n**During Meeting:**\n• Meet in campus libraries or cafes\n• Bring a friend for extra safety\n• Inspect items thoroughly before paying\n• Use secure payment methods\n• Keep your phone charged and accessible\n\n**After Meeting:**\n• Leave honest reviews\n• Report any issues immediately\n• Block users who made you uncomfortable\n• Keep all communication records\n• Trust your gut feeling\n\n**Emergency Contacts:**\n• Campus security: Available 24/7\n• EduCycle support: support@educycle.com\n• Local police: For serious incidents\n\n⚠️ **Remember**: If something feels wrong, don't proceed!",
                    
                    "⚠️ **Safety First - Always:**\n\n**Ideal Meeting Spots:**\n• Campus libraries (most secure)\n• Student centers and lounges\n• Public cafes with good lighting\n• Shopping centers and malls\n• Busy restaurants\n\n**What to Avoid:**\n• Isolated parking lots\n• Private residences\n• Dark or secluded areas\n• Late night meetings\n• Pressure to meet quickly\n\n**Payment Security:**\n• Inspect items thoroughly before payment\n• Use cash or verified digital payments\n• Never share bank account details\n• Keep all transaction records\n• Don't pay before seeing the item\n\n**Trust Your Instincts:**\n• If something feels off, don't proceed\n• It's okay to walk away\n• Report suspicious behavior\n• Block users who make you uncomfortable\n• Your safety comes first\n\n**Emergency Protocol:**\n• Leave immediately if unsafe\n• Contact campus security\n• Report to EduCycle support\n• Keep all evidence and records\n\n🛡️ **Your safety is non-negotiable!**"
                ]
            },
            'payment': {
                'patterns': ['payment', 'pay', 'money', 'price', 'cost', 'payment method', 'cash', 'digital', 'wallet', 'payment methods', 'how to pay', 'accepted payments'],
                'responses': [
                    "💳 **Complete Payment Guide:**\n\n**Accepted Payment Methods:**\n• **Cash** (most recommended for local meetups)\n• **Digital Wallets**: PayTM, Google Pay, PhonePe, Apple Pay\n• **Online Payments**: Through our secure payment gateway\n• **Bank Transfers**: Direct transfers (arranged with seller)\n• **UPI**: Instant digital payments\n\n**Payment Process:**\n1. **Agree on Price**: Negotiate and confirm final price\n2. **Choose Method**: Decide on payment method together\n3. **Meet Safely**: Choose public, well-lit location\n4. **Verify Item**: Inspect item thoroughly before payment\n5. **Complete Payment**: Exchange money and item\n6. **Keep Records**: Save all transaction details\n\n**Payment Safety Tips:**\n• Always verify item condition before paying\n• Use secure, traceable payment methods\n• Keep all transaction records and receipts\n• Meet in public places for cash transactions\n• Never share sensitive financial information\n• Trust your instincts - if payment method seems suspicious, don't proceed\n\n💡 **Pro Tip**: Cash is safest for local meetups, digital payments for convenience!",
                    
                    "💰 **Payment Options Explained:**\n\n**Cash Payments:**\n• Most common for local meetups\n• No transaction fees\n• Immediate exchange\n• Requires physical meeting\n• Keep exact change ready\n\n**Digital Wallets:**\n• PayTM, Google Pay, PhonePe\n• Instant transfers\n• Transaction records\n• Works for remote payments\n• Secure and traceable\n\n**Online Payments:**\n• Through EduCycle's secure gateway\n• Protected by platform security\n• Transaction records maintained\n• Works for all transactions\n• Platform protection included\n\n**Bank Transfers:**\n• Direct account-to-account\n• Lower fees than digital wallets\n• Requires account details\n• Good for larger amounts\n• Keep transfer receipts\n\n**Safety Guidelines:**\n• Verify items before any payment\n• Use secure, traceable methods\n• Keep all transaction records\n• Meet in public places\n• Never share sensitive financial info\n\n✅ **Remember**: Payment method is agreed between buyers and sellers!",
                    
                    "💸 **Smart Payment Strategies:**\n\n**For Local Meetups:**\n• **Cash**: Most straightforward, no fees\n• **Digital Wallets**: Convenient, traceable\n• **UPI**: Instant, widely accepted\n\n**For Remote Transactions:**\n• **Online Payments**: Platform protection\n• **Digital Wallets**: Quick and secure\n• **Bank Transfers**: For larger amounts\n\n**Payment Best Practices:**\n• Discuss payment method before meeting\n• Agree on exact amount and method\n• Verify item condition before paying\n• Use secure, traceable methods\n• Keep all transaction records\n• Get receipts when possible\n\n**Security Tips:**\n• Never share bank account details\n• Use secure payment apps\n• Meet in public places\n• Trust your instincts\n• Report suspicious payment requests\n\n**What to Avoid:**\n• Sharing sensitive financial information\n• Paying before seeing the item\n• Using untraceable payment methods\n• Meeting in isolated locations\n• Pressure to pay quickly\n\n🎯 **Goal**: Safe, secure, and convenient payments for everyone!"
                ]
            },
            'categories': {
                'patterns': ['category', 'categories', 'what can I sell', 'what can I buy', 'types of items', 'items', 'products'],
                'responses': [
                    "📚 **EduCycle Categories:**\n\n**Academic Items:**\n• Textbooks and study materials\n• Lab equipment and supplies\n• Scientific calculators\n• Stationery and notebooks\n\n**Electronics:**\n• Laptops and computers\n• Mobile phones and accessories\n• Gaming consoles\n• Audio equipment\n\n**Furniture & Decor:**\n• Room furniture and decor\n• Mini-fridges and appliances\n• Lighting and lamps\n• Storage solutions\n\n**Sports & Fitness:**\n• Sports equipment\n• Gym accessories\n• Bicycles and vehicles\n• Fitness gear\n\n**And much more!**",
                    
                    "🛍️ **What You Can Buy/Sell:**\n\n**Study Materials:**\n• Textbooks, notebooks, stationery\n• Lab coats, safety equipment\n• Scientific calculators\n• Study guides and notes\n\n**Electronics:**\n• Laptops, tablets, phones\n• Gaming devices\n• Audio/visual equipment\n• Chargers and accessories\n\n**Lifestyle:**\n• Room decor and furniture\n• Kitchen appliances\n• Clothing and accessories\n• Sports and fitness equipment\n\n**Everything students need!**",
                    
                    "📦 **Item Categories:**\n\n**Academic:**\n• Textbooks and reference books\n• Lab equipment and supplies\n• Study materials and notes\n• Scientific calculators\n\n**Electronics:**\n• Computers and laptops\n• Mobile devices\n• Gaming equipment\n• Audio/visual gear\n\n**Lifestyle:**\n• Room furniture and decor\n• Kitchen and home appliances\n• Sports and fitness equipment\n• Clothing and accessories\n\n**Student Essentials:**\n• Backpacks and bags\n• Stationery and supplies\n• Room organization items\n• Transportation (bikes, etc.)"
                ]
            },
            'contact': {
                'patterns': ['contact', 'support', 'help desk', 'customer service', 'report', 'bug', 'issue', 'problem', 'contact support', 'how do i contact', 'get help'],
                'responses': [
                    "📞 **Complete Support Guide:**\n\n**Help Resources Available:**\n• **Help Center**: Browse common questions and tutorials\n• **Contact Us Page**: General inquiries and feedback\n• **Report a Bug**: Technical issues and platform problems\n• **Email Support**: support@educycle.com\n• **Chat Support**: You're using it right now!\n\n**How to Get Help:**\n1. **Check Help Center First**: Most questions are answered here\n2. **Use Contact Us**: For general inquiries and feedback\n3. **Report Bugs**: For technical issues and platform problems\n4. **Email Support**: For urgent matters and complex issues\n5. **Chat Support**: For immediate assistance (like now!)\n\n**Response Times:**\n• **Help Center**: Immediate access to answers\n• **Contact Us**: 24-48 hours response\n• **Bug Reports**: 1-3 business days\n• **Email Support**: 24 hours\n• **Chat Support**: Real-time assistance\n\n**What to Include:**\n• Clear description of your issue\n• Screenshots if applicable\n• Steps to reproduce the problem\n• Your account details (if relevant)\n• Contact information for follow-up\n\n💬 **Chat Support**: You're getting help right now!",
                    
                    "🆘 **Support Options & Channels:**\n\n**Self-Service Resources:**\n• **Help Center**: Comprehensive guides and FAQs\n• **FAQ Section**: Quick answers to common questions\n• **User Guides**: Step-by-step tutorials\n• **Video Tutorials**: Visual learning resources\n• **Community Forum**: Peer-to-peer help\n\n**Direct Contact Methods:**\n• **Contact Us Page**: General inquiries and feedback\n• **Report a Bug Form**: Technical issues and platform problems\n• **Email Support**: support@educycle.com\n• **Chat Support**: Real-time assistance (current)\n• **Social Media**: Follow us for updates and tips\n\n**Response Time Expectations:**\n• **Help Center**: Instant access to information\n• **Contact Forms**: 24-48 hours response\n• **Email Support**: 24 hours\n• **Bug Reports**: 1-3 business days\n• **Chat Support**: Real-time (immediate)\n\n**Emergency Support:**\n• **Urgent Issues**: Email with 'URGENT' in subject\n• **Security Issues**: Immediate attention\n• **Account Problems**: 24-hour response\n• **Technical Emergencies**: Priority handling\n\n✅ **We're committed to helping you succeed!**",
                    
                    "📋 **Support Channels & Best Practices:**\n\n**Help Center (Recommended First):**\n• Browse common questions and solutions\n• Step-by-step guides for all features\n• Troubleshooting tips and tricks\n• Video tutorials and demonstrations\n• Best practices and tips\n\n**Contact Options:**\n• **Contact Us Page**: General inquiries and feedback\n• **Report a Bug Form**: Technical issues and problems\n• **Email Support**: support@educycle.com\n• **Chat Support**: Real-time assistance (you're here!)\n\n**Response Time Guarantees:**\n• **Help Center**: Immediate access to answers\n• **Contact Forms**: 24-48 hours response\n• **Email Support**: 24 hours\n• **Bug Reports**: 1-3 business days\n• **Chat Support**: Real-time assistance\n\n**Getting the Best Help:**\n• **Be Specific**: Describe your issue clearly\n• **Include Details**: Screenshots, error messages, steps\n• **Provide Context**: What you were trying to do\n• **Follow Up**: Respond to support team questions\n• **Be Patient**: Complex issues may take time\n\n**Pro Tips:**\n• Check Help Center first - 80% of issues are solved there\n• Include screenshots for technical problems\n• Be polite and patient with support staff\n• Keep records of your support requests\n\n💡 **Tip**: Help Center has answers to most common questions!"
                ]
            },
            'reviews': {
                'patterns': ['review', 'rating', 'feedback', 'star', 'rate', 'comment', 'opinion', 'reviews work', 'how do reviews', 'rating system'],
                'responses': [
                    "⭐ **Complete Review & Rating Guide:**\n\n**Leaving Great Reviews:**\n• **Rate Items**: Give 1-5 stars based on experience\n• **Share Details**: Describe what you liked/disliked\n• **Be Specific**: Mention item condition, seller communication\n• **Include Photos**: Add pictures if relevant\n• **Be Honest**: Accurate reviews help everyone\n• **Be Constructive**: Helpful feedback improves the community\n\n**Reading Reviews Effectively:**\n• **Check Seller Ratings**: Look for 4+ star average\n• **Read Recent Reviews**: Focus on latest feedback\n• **Look for Patterns**: Consistent issues or praise\n• **Consider Context**: Understand the specific situation\n• **Check Response Rate**: Sellers who respond to reviews\n\n**Review Guidelines:**\n• **Be Honest**: Don't inflate or deflate ratings\n• **Be Specific**: Include relevant details\n• **Be Fair**: Rate based on actual experience\n• **Be Helpful**: Provide constructive feedback\n• **Be Timely**: Leave reviews within a week\n\n**Review Benefits:**\n• Help other buyers make informed decisions\n• Build trust in the community\n• Improve seller reputation\n• Create a better platform for everyone\n\n💡 **Pro Tip**: Detailed, honest reviews are worth their weight in gold!",
                    
                    "📝 **Smart Review System:**\n\n**For Buyers - How to Leave Great Reviews:**\n• **Rate Promptly**: Leave review within a week of purchase\n• **Be Detailed**: Describe item condition, seller communication\n• **Include Photos**: Show what you received\n• **Rate Fairly**: Consider price, condition, and expectations\n• **Be Honest**: Don't inflate ratings for friends\n• **Help Others**: Your review helps future buyers\n\n**For Sellers - Managing Your Reviews:**\n• **Respond Promptly**: Address concerns within 24 hours\n• **Be Professional**: Stay calm and helpful\n• **Learn from Feedback**: Use reviews to improve\n• **Build Reputation**: Good reviews attract more buyers\n• **Address Issues**: Fix problems mentioned in reviews\n\n**Review Best Practices:**\n• **Be Specific**: Mention exact details about experience\n• **Include Both Sides**: Pros and cons when relevant\n• **Rate Honestly**: Don't let emotions cloud judgment\n• **Help the Community**: Your review builds trust\n• **Follow Guidelines**: Respect platform review policies\n\n**Review Impact:**\n• **For Buyers**: Make informed purchasing decisions\n• **For Sellers**: Build credibility and attract customers\n• **For Platform**: Create trustworthy marketplace\n• **For Community**: Foster honest, helpful environment\n\n✅ **Great reviews create a great community!**",
                    
                    "🌟 **Rating System & Community Trust:**\n\n**How the Rating System Works:**\n• **1-5 Star Scale**: Rate items and sellers\n• **Detailed Comments**: Explain your rating\n• **Photo Evidence**: Include pictures when relevant\n• **Timely Reviews**: Leave feedback within a week\n• **Honest Assessment**: Rate based on actual experience\n\n**Writing Effective Reviews:**\n• **Be Honest**: Don't inflate or deflate ratings\n• **Be Specific**: Include relevant details and context\n• **Be Constructive**: Provide helpful feedback\n• **Be Fair**: Consider price, condition, and expectations\n• **Be Timely**: Leave reviews while experience is fresh\n\n**Reading Reviews Like a Pro:**\n• **Check Overall Rating**: Look for 4+ star averages\n• **Read Recent Reviews**: Focus on latest feedback\n• **Look for Patterns**: Consistent praise or issues\n• **Consider Context**: Understand the specific situation\n• **Check Seller Response**: How they handle feedback\n\n**Review Guidelines & Standards:**\n• **No Fake Reviews**: Only review items you've actually purchased\n• **No Personal Attacks**: Focus on the item and experience\n• **Be Respectful**: Even negative reviews should be constructive\n• **Follow Platform Rules**: Respect review policies\n• **Help the Community**: Your review helps others\n\n**Benefits of Great Reviews:**\n• **Better Decisions**: Make informed purchasing choices\n• **Build Trust**: Create reliable marketplace reputation\n• **Improve Quality**: Feedback helps sellers improve\n• **Community Growth**: Honest reviews attract more users\n• **Platform Success**: Trustworthy reviews build platform value\n\n🎯 **Goal**: Create the most trusted student marketplace through honest reviews!"
                ]
            },
            'pricing': {
                'patterns': ['price', 'pricing', 'cost', 'expensive', 'cheap', 'value', 'worth', 'fair price', 'help with pricing', 'pricing strategy', 'set price'],
                'responses': [
                    "💰 **Pricing Guidelines:**\n\n**Setting Prices:**\n• Research similar items\n• Consider item condition\n• Factor in original cost\n• Be competitive but fair\n\n**Price Factors:**\n• Item condition (new/used)\n• Original purchase price\n• Market demand\n• Seller reputation\n\n**Pricing Tips:**\n• Check similar listings\n• Consider depreciation\n• Be realistic about condition\n• Start competitive, adjust if needed\n\n💡 **Tip**: Fair pricing attracts more buyers!",
                    
                    "💵 **Pricing Strategy:**\n\n**Research First:**\n• Check similar items\n• Compare conditions\n• Look at seller ratings\n• Consider market demand\n\n**Setting Your Price:**\n• Factor in item condition\n• Consider original cost\n• Be competitive\n• Allow for negotiation\n\n**Price Adjustment:**\n• Monitor similar listings\n• Adjust based on interest\n• Consider time sensitivity\n• Be flexible with serious buyers\n\n✅ **Fair pricing = faster sales!**",
                    
                    "📊 **Pricing Guide:**\n\n**Market Research:**\n• Check similar items\n• Compare conditions\n• Look at seller ratings\n• Consider demand\n\n**Price Setting:**\n• Factor in condition\n• Consider original cost\n• Be competitive\n• Allow negotiation\n\n**Price Management:**\n• Monitor market trends\n• Adjust based on interest\n• Consider time factors\n• Be flexible with buyers"
                ]
            },
            'shipping': {
                'patterns': ['shipping', 'delivery', 'pickup', 'meet', 'location', 'where', 'transport', 'meet buyers', 'meet sellers', 'where to meet', 'meeting location'],
                'responses': [
                    "🚚 **Pickup & Delivery:**\n\n**Local Pickup (Recommended):**\n• Meet in safe, public locations\n• Campus libraries and cafes\n• Student centers and common areas\n• Well-lit, populated places\n\n**Delivery Options:**\n• Arrange with seller directly\n• Campus delivery (if available)\n• Public meeting points\n• Safe exchange locations\n\n**Safety Tips:**\n• Always meet in public places\n• Bring a friend if possible\n• Trust your instincts\n• Report any issues\n\n✅ **Safety first, always!**",
                    
                    "📍 **Meeting Locations:**\n\n**Safe Meeting Spots:**\n• Campus libraries\n• Student cafes\n• Public restaurants\n• Shopping centers\n• Well-lit areas\n\n**Delivery Arrangements:**\n• Coordinate with seller\n• Choose safe locations\n• Verify item before payment\n• Keep communication records\n\n**Safety Guidelines:**\n• Meet in public places\n• Avoid isolated locations\n• Bring someone if possible\n• Trust your instincts\n\n⚠️ **Never meet in isolated areas!**",
                    
                    "🚛 **Pickup & Delivery Guide:**\n\n**Local Pickup:**\n• Meet in public places\n• Campus libraries and cafes\n• Student centers\n• Well-lit areas\n\n**Delivery Options:**\n• Arrange with seller\n• Safe meeting points\n• Public locations\n• Verified exchange spots\n\n**Safety First:**\n• Always public locations\n• Bring friend if possible\n• Trust your instincts\n• Report suspicious behavior"
                ]
            },
            'technical': {
                'patterns': ['technical', 'bug', 'error', 'problem', 'issue', 'not working', 'broken', 'fix'],
                'responses': [
                    "🔧 **Technical Support:**\n\n**Common Issues:**\n• Login problems\n• Upload issues\n• Payment errors\n• Message delivery\n• App performance\n\n**Troubleshooting:**\n1. Clear browser cache\n2. Check internet connection\n3. Try different browser\n4. Restart application\n\n**Getting Help:**\n• Report a Bug form\n• Email: support@educycle.com\n• Include error details\n• Provide screenshots\n\n⏰ **Response**: Technical issues resolved within 24-48 hours",
                    
                    "🛠️ **Technical Issues:**\n\n**Quick Fixes:**\n• Refresh the page\n• Clear browser cache\n• Check internet connection\n• Try different browser\n\n**Common Problems:**\n• Login issues\n• Upload failures\n• Payment errors\n• Message problems\n• Performance issues\n\n**Reporting Issues:**\n• Use Report a Bug form\n• Include error details\n• Provide screenshots\n• Describe steps to reproduce\n\n📧 **Email**: support@educycle.com for urgent issues",
                    
                    "💻 **Technical Help:**\n\n**Self-Fix Steps:**\n• Refresh the page\n• Clear browser cache\n• Check internet connection\n• Try different browser\n\n**Common Issues:**\n• Login problems\n• Upload failures\n• Payment errors\n• Message delivery\n• Performance issues\n\n**Report Problems:**\n• Use Report a Bug form\n• Include error details\n• Provide screenshots\n• Email for urgent issues"
                ]
            }
        }

    def get_response(self, user_message, session_id):
        """Get chatbot response based on user message"""
        # Save user message
        ChatMessage.objects.create(
            session_id=session_id,
            message_type='user',
            content=user_message
        )
        
        # Process message and get response
        response = self._process_message(user_message.lower())
        
        # Save bot response
        ChatMessage.objects.create(
            session_id=session_id,
            message_type='bot',
            content=response
        )
        
        return response

    def _process_message(self, message):
        """Process user message and return appropriate response"""
        # Check for greetings
        if any(greeting in message for greeting in self.greetings):
            return random.choice(self.conversation_flows['greeting']['responses'])
        
        # Check for farewells
        if any(farewell in message for farewell in self.farewells):
            return random.choice(self.conversation_flows['farewell']['responses'])
        
        # Check for specific topics with improved pattern matching
        for topic, flow in self.conversation_flows.items():
            if topic not in ['greeting', 'farewell']:
                if any(pattern in message for pattern in flow['patterns']):
                    return random.choice(flow['responses'])
        
        # Check for help keywords (after specific topics)
        if any(help_word in message for help_word in self.help_keywords):
            return self._get_help_response()
        
        # Check for natural language queries
        if self._is_natural_language_query(message):
            return self._get_natural_language_response(message)
        
        # Check for specific questions about items
        if any(word in message for word in ['item', 'product', 'listing']):
            return self._get_item_info_response()
        
        # Check for account-related questions
        if any(word in message for word in ['password', 'reset', 'forgot', 'change']):
            return self._get_account_help_response()
        
        # Check for payment-related questions
        if any(word in message for word in ['refund', 'return', 'money back']):
            return self._get_refund_response()
        
        # Check for platform statistics
        if any(word in message for word in ['stats', 'statistics', 'how many', 'count', 'users', 'items']):
            return self.get_quick_stats()
        
        # Check for urgent/support queries
        if any(word in message for word in ['urgent', 'emergency', 'immediate', 'critical', 'broken', 'hacked']):
            return self._get_urgent_support_response()
        
        # Check for general platform questions
        if any(word in message for word in ['platform', 'website', 'app', 'mobile', 'desktop']):
            return self._get_platform_info_response()
        
        # Default response for unrecognized messages
        return self._get_default_response()

    def _get_help_response(self):
        """Get comprehensive help response"""
        return """🤖 **I'm here to help! Here's what I can assist you with:**

🛒 **Buying & Selling**
• How to buy items
• How to sell items
• Payment methods
• Safety guidelines
• Pricing strategies

👤 **Account Management**
• Creating an account
• Login/logout help
• Profile settings
• Password reset

📚 **Platform Features**
• Item categories
• Search and filters
• Reviews and ratings
• Contact sellers

🛡️ **Safety & Support**
• Safety guidelines
• Meeting safely
• Contact support
• Report issues

💬 **Reviews & Community**
• Leaving reviews
• Reading reviews
• Building trust
• Community guidelines

🔧 **Technical Help**
• Bug reports
• Technical issues
• App problems
• Performance issues

**Just ask me about any of these topics, or try one of the suggested questions below!**"""

    def _get_item_info_response(self):
        """Get response about items and listings"""
        return """📦 **About Items & Listings:**

**What You Can Buy/Sell:**
• Textbooks and study materials
• Electronics and gadgets
• Room decor and furniture
• Sports equipment
• Lab supplies and equipment
• And much more!

**Creating Good Listings:**
• Clear, detailed descriptions
• High-quality photos
• Accurate pricing
• Honest condition assessment
• Quick responses to buyers

**Finding Items:**
• Use search filters
• Browse categories
• Check seller ratings
• Read item descriptions
• Ask sellers questions

💡 **Tip**: Good photos and detailed descriptions help items sell faster!"""

    def _get_account_help_response(self):
        """Get response for account-related issues"""
        return """🔐 **Account Help:**

**Password Issues:**
• Use 'Forgot Password' link
• Check your email for reset link
• Create a strong new password
• Contact support if needed

**Login Problems:**
• Check your email/username
• Ensure caps lock is off
• Clear browser cache
• Try different browser

**Account Security:**
• Use strong passwords
• Enable two-factor if available
• Keep contact info updated
• Report suspicious activity

**Profile Management:**
• Update personal information
• Add profile picture
• Manage notification settings
• Update student details

📧 **Need more help?** Contact support@educycle.com"""

    def _get_refund_response(self):
        """Get response about refunds and returns"""
        return """💰 **Refunds & Returns:**

**Our Policy:**
• Refunds are arranged between buyers and sellers
• EduCycle facilitates communication
• No automatic refunds
• Disputes resolved case-by-case

**If You Need a Refund:**
1. Contact the seller directly
2. Explain the issue clearly
3. Provide evidence if needed
4. Try to resolve amicably
5. Contact support if unresolved

**Preventing Issues:**
• Verify items before paying
• Ask detailed questions
• Check seller ratings
• Meet in safe locations
• Keep all communication records

**Support Process:**
• Contact support with details
• Include transaction information
• Provide evidence of issues
• We'll mediate the dispute

⚠️ **Remember**: Always verify items before payment!"""

    def _get_default_response(self):
        """Get improved default response"""
        default_responses = [
            "I'm not sure I understood that. Could you try asking about buying, selling, account setup, safety, payment methods, or technical issues?",
            "I didn't catch that. You can ask me about how to buy/sell items, create an account, safety guidelines, payment methods, or platform features.",
            "I'm here to help with EduCycle! Try asking about buying, selling, account setup, safety, payment methods, or how to use our platform.",
            "Not sure what you mean. I can help with buying/selling, account questions, safety guidelines, payment methods, or technical issues. What would you like to know?",
            "I'm your EduCycle assistant! I can help with buying, selling, account management, safety, payments, or technical support. What do you need help with?"
        ]
        return random.choice(default_responses)

    def get_conversation_history(self, session_id):
        """Get conversation history for a session"""
        return ChatMessage.objects.filter(session_id=session_id).order_by('timestamp')

    def get_suggested_questions(self):
        """Get enhanced suggested questions"""
        return [
            "How do I buy items?",
            "How do I sell items?",
            "How do I create an account?",
            "Is it safe to meet sellers?",
            "What payment methods are accepted?",
            "What can I buy and sell?",
            "How do I contact support?",
            "How do reviews work?",
            "How do I set a good price?",
            "Where should I meet buyers/sellers?",
            "What if I have technical issues?",
            "How do refunds work?"
        ]

    def get_welcome_message(self):
        """Get enhanced welcome message"""
        return """👋 **Welcome to EduCycle! I'm your AI assistant here to help you navigate our student marketplace.**

I can help you with:

🛒 **Buying & Selling**
• How to buy and sell items
• Payment methods and safety
• Pricing strategies
• Meeting arrangements

👤 **Account Management**
• Creating and managing accounts
• Profile settings
• Login/logout help
• Password reset

📚 **Platform Features**
• Item categories and search
• Reviews and ratings
• Contact sellers
• Platform navigation

🛡️ **Safety & Support**
• Safety guidelines
• Meeting safely
• Contact support
• Report issues

💬 **Community**
• Reviews and feedback
• Building trust
• Community guidelines
• Best practices

**Try asking me about any of these topics, or use the suggested questions below to get started!**

What would you like to know about EduCycle?""" 

    def get_quick_stats(self):
        """Get quick platform statistics"""
        try:
            total_items = Item.objects.filter(is_active=True).count()
            total_users = User.objects.count()
            total_orders = Order.objects.count()
            
            return f"""📊 **EduCycle Quick Stats:**
• Active Items: {total_items}
• Registered Users: {total_users}
• Completed Orders: {total_orders}
• Categories: 5+ (Textbooks, Electronics, Furniture, Sports, More)

💡 **Join our growing community!**"""
        except:
            return "📊 **EduCycle is growing fast! Join our community of students buying and selling items.**"

    def _get_urgent_support_response(self):
        """Get response for urgent support queries"""
        return """🚨 **Urgent Support:**

**For Immediate Issues:**
• Email: support@educycle.com
• Include 'URGENT' in subject line
• Provide detailed description
• Include screenshots if possible

**Security Issues:**
• Report suspicious activity immediately
• Change your password if compromised
• Contact support with details
• Block problematic users

**Technical Emergencies:**
• Clear browser cache and cookies
• Try different browser
• Check internet connection
• Contact support with error details

**Response Time:**
• Urgent emails: 2-4 hours
• Security issues: 1-2 hours
• Technical problems: 4-8 hours

📧 **Email**: support@educycle.com (mark as URGENT)"""

    def _get_platform_info_response(self):
        """Get response about platform features"""
        return """🌐 **EduCycle Platform:**

**Web Platform:**
• Access via any web browser
• Mobile-responsive design
• Works on all devices
• No app download required

**Key Features:**
• Real-time messaging
• Secure payment processing
• User reviews and ratings
• Advanced search filters
• Image upload support
• Notification system

**Browser Compatibility:**
• Chrome (recommended)
• Firefox
• Safari
• Edge
• Mobile browsers

**Platform Updates:**
• Regular security updates
• New features added monthly
• Performance improvements
• User feedback integration

💡 **Tip**: Use Chrome for the best experience!"""

    def _is_natural_language_query(self, message):
        """Check if message is a natural language query"""
        natural_indicators = [
            'can you', 'could you', 'would you', 'please', 'i need', 'i want',
            'how can', 'what should', 'where do', 'when can', 'why does',
            'tell me', 'explain', 'describe', 'show me', 'help me'
        ]
        return any(indicator in message for indicator in natural_indicators)

    def _get_natural_language_response(self, message):
        """Get response for natural language queries"""
        if any(word in message for word in ['buy', 'purchase', 'shop']):
            return random.choice(self.conversation_flows['buying']['responses'])
        elif any(word in message for word in ['sell', 'list', 'post', 'upload']):
            return random.choice(self.conversation_flows['selling']['responses'])
        elif any(word in message for word in ['account', 'register', 'sign up', 'login']):
            return random.choice(self.conversation_flows['account']['responses'])
        elif any(word in message for word in ['safe', 'safety', 'secure', 'trust']):
            return random.choice(self.conversation_flows['safety']['responses'])
        elif any(word in message for word in ['pay', 'payment', 'money', 'cost']):
            return random.choice(self.conversation_flows['payment']['responses'])
        elif any(word in message for word in ['category', 'item', 'product', 'type']):
            return random.choice(self.conversation_flows['categories']['responses'])
        elif any(word in message for word in ['contact', 'support', 'help', 'report']):
            return random.choice(self.conversation_flows['contact']['responses'])
        elif any(word in message for word in ['review', 'rating', 'feedback']):
            return random.choice(self.conversation_flows['reviews']['responses'])
        else:
            return self._get_default_response() 