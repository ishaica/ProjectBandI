document.addEventListener('DOMContentLoaded', () => {
    const cornerLinkDiv = document.querySelector('.corner_links');
    const title = document.querySelector('.title');

    if (!(cornerLinkDiv && title)) return;

    const linkElements = cornerLinkDiv.getElementsByTagName('a');

    const handleMouseEnter = (element) => {
        element.style.color = '#c2b0f0';
        element.style.transition = 'color 0.2s ease';
    };

    const handleMouseLeave = (element) => {
        element.style.color = 'initial';
    };

    const handleTitleMouseEnter = () => {
        title.style.color = '#c2b0f0';
        title.style.transition = 'color 0.2s ease';
    };

    const handleTitleMouseLeave = () => {
        title.style.color = 'initial';
    };

    if (linkElements.length) {  // Fixed the if condition
        Array.from(linkElements).forEach(link => {
            link.addEventListener('mouseenter', () => handleMouseEnter(link));
            link.addEventListener('mouseleave', () => handleMouseLeave(link));
        });
        
        title.addEventListener('mouseenter', handleTitleMouseEnter);
        title.addEventListener('mouseleave', handleTitleMouseLeave);
    }
});