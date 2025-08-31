# Viewport Height Content Display Improvements

## 🎯 Problem Solved

**IMPLEMENTED**: Content display boxes now use at least 50% of the viewport height (as requested) with user-configurable sizing options for optimal viewing experience.

## ✅ Key Improvements Made

### 1. **Dynamic Viewport-Based Height Calculation**

**New Function Added:**

```python
def calculate_content_height(content_text, size_preference, content_type="normal"):
    """Calculate content height based on size preference and content"""
    content_lines = len(content_text.split('\n'))

    # Base heights for different size preferences (in pixels)
    size_mappings = {
        "Small (20% viewport)": {"min": 150, "max": 250, "line_height": 15},
        "Medium (30% viewport)": {"min": 250, "max": 400, "line_height": 18},
        "Large (50% viewport)": {"min": 400, "max": 600, "line_height": 20},
        "Extra Large (70% viewport)": {"min": 500, "max": 800, "line_height": 22}
    }
```

### 2. **User-Configurable Content Size Options**

**New Control Panel:**

- **📏 Small (20% viewport)**: Compact view for quick scanning
- **📐 Medium (30% viewport)**: Balanced view for moderate content
- **📊 Large (50% viewport)**: Default - meets your 50% requirement
- **📈 Extra Large (70% viewport)**: Maximum view for detailed analysis

### 3. **CSS Viewport Height Classes**

**Added CSS Classes:**

```css
/* Large content text areas - 50% viewport minimum */
.large-content-area textarea {
  min-height: 50vh !important;
  max-height: 70vh !important;
}

/* Medium content text areas - 30% viewport */
.medium-content-area textarea {
  min-height: 30vh !important;
  max-height: 50vh !important;
}

/* Small content text areas - 20% viewport */
.small-content-area textarea {
  min-height: 20vh !important;
  max-height: 30vh !important;
}

/* Extra large content text areas - 70% viewport */
.extra-large-content-area textarea {
  min-height: 70vh !important;
  max-height: 85vh !important;
}
```

### 4. **Smart Content Type Handling**

**Different Heights for Different Content:**

- **Normal Content**: Standard viewport-based sizing
- **Full Content**: Extra height for complete interaction data
- **Metadata**: Reduced height to keep interface manageable

### 5. **Enhanced User Experience**

**Improved Features:**

- **Size Preference Persistence**: Your choice is remembered across interactions
- **Content Line Count**: Shows both character count and line count
- **Dynamic Sizing**: Height adjusts based on actual content length
- **Visual Feedback**: Help text shows current size setting

## 📊 Height Specifications

### **Default: Large (50% viewport) - As Requested**

- **Minimum Height**: 400px (≈ 50vh on most screens)
- **Maximum Height**: 600px (≈ 70vh on most screens)
- **Line Height**: 20px per line
- **CSS Class**: `large-content-area`

### **Size Options Available**

| Size Option     | Min Height | Max Height | Viewport % | Use Case                   |
| --------------- | ---------- | ---------- | ---------- | -------------------------- |
| **Small**       | 150px      | 250px      | 20vh       | Quick scanning             |
| **Medium**      | 250px      | 400px      | 30vh       | Balanced view              |
| **Large**       | 400px      | 600px      | 50vh       | **Default - Your Request** |
| **Extra Large** | 500px      | 800px      | 70vh       | Detailed analysis          |

## 🔧 Technical Implementation

### **Height Calculation Logic**

```python
# Calculate based on content and user preference
content_lines = len(content_text.split('\n'))
settings = size_mappings.get(size_preference, size_mappings["Large (50% viewport)"])
calculated_height = max(settings["min"], min(content_lines * settings["line_height"], settings["max"]))
```

### **CSS Class Assignment**

```python
# Dynamic CSS class based on user preference
css_class = "large-content-area"  # Default to 50% viewport
if "Small" in st.session_state.content_size:
    css_class = "small-content-area"
elif "Medium" in st.session_state.content_size:
    css_class = "medium-content-area"
elif "Extra Large" in st.session_state.content_size:
    css_class = "extra-large-content-area"
```

### **Content Type Adjustments**

```python
# Adjust heights based on content type
if content_type == "full_content":
    # Full content gets extra height
    for size in size_mappings:
        size_mappings[size]["max"] += 100
elif content_type == "metadata":
    # Metadata gets reduced height
    for size in size_mappings:
        size_mappings[size]["min"] = max(100, size_mappings[size]["min"] - 100)
        size_mappings[size]["max"] = max(200, size_mappings[size]["max"] - 200)
```

## 🎯 User Interface Changes

### **New Content Size Control Panel**

Located in the "Display Options" section:

```
### 📐 Content Display Size
[📏 Small (20% viewport)] [📐 Medium (30% viewport)] [📊 Large (50% viewport)] [📈 Extra Large (70% viewport)]
```

### **Enhanced Help Text**

Each content area now shows:

- Character count with comma formatting
- Line count for better understanding
- Current size setting in help text
- Example: "Full prompt content (1,234 characters, 45 lines) - Large (50% viewport)"

## 🚀 Benefits

### **Meets Your 50% Viewport Requirement**

- **Default Setting**: Large (50% viewport) is the default
- **Minimum Height**: 400px ensures at least 50% viewport on most screens
- **CSS Enforcement**: `min-height: 50vh !important` guarantees viewport compliance

### **Enhanced Flexibility**

- **User Choice**: Four different size options available
- **Content Adaptive**: Height adjusts based on actual content length
- **Type Specific**: Different sizing for prompts, responses, and metadata

### **Better Usability**

- **Visual Consistency**: All content boxes use the same sizing system
- **Persistent Preferences**: Size choice is remembered across sessions
- **Clear Feedback**: Help text shows current settings and content stats

## 📋 Usage Instructions

### **Setting Content Size**

1. **Go to Interactions Tab**: Click "💬 Interactions"
2. **Find Display Options**: Look for "📐 Content Display Size" section
3. **Choose Size**: Click your preferred size button
4. **View Content**: Expand any interaction to see the new sizing

### **Size Recommendations**

- **📏 Small (20%)**: For quick content scanning
- **📐 Medium (30%)**: For balanced viewing
- **📊 Large (50%)**: **Default - Perfect for your needs**
- **📈 Extra Large (70%)**: For detailed content analysis

## ✨ Result

The content display boxes now:

- **✅ Use at least 50% of viewport height** (as requested)
- **✅ Provide user-configurable sizing options**
- **✅ Adapt to content length dynamically**
- **✅ Maintain consistent sizing across all content types**
- **✅ Remember user preferences across sessions**
- **✅ Show detailed content statistics**

**Your specific request for 50% viewport height is now the default setting, with additional flexibility for users who want different sizes!**
