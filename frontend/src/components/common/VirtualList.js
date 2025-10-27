import React from "react";
import { jsx as _jsx } from "react/jsx-runtime";
import { useRef, useState, useEffect } from 'react';
/**
 * Virtual list component for rendering large lists efficiently
 * Only renders items that are currently visible in the viewport
 */
export function VirtualList({ items, itemHeight, containerHeight, renderItem, overscan = 3 }) {
    const containerRef = useRef(null);
    const [scrollTop, setScrollTop] = useState(0);
    // Calculate visible range
    const startIndex = Math.max(0, Math.floor(scrollTop / itemHeight) - overscan);
    const endIndex = Math.min(items.length - 1, Math.ceil((scrollTop + containerHeight) / itemHeight) + overscan);
    const visibleItems = items.slice(startIndex, endIndex + 1);
    const totalHeight = items.length * itemHeight;
    const offsetY = startIndex * itemHeight;
    useEffect(() => {
        const container = containerRef.current;
        if (!container)
            return;
        const handleScroll = () => {
            setScrollTop(container.scrollTop);
        };
        container.addEventListener('scroll', handleScroll);
        return () => container.removeEventListener('scroll', handleScroll);
    }, []);
    return (_jsx("div", { ref: containerRef, style: {
            height: containerHeight,
            overflow: 'auto',
            position: 'relative'
        }, children: _jsx("div", { style: { height: totalHeight, position: 'relative' }, children: _jsx("div", { style: {
                    transform: `translateY(${offsetY}px)`,
                    willChange: 'transform'
                }, children: visibleItems.map((item, idx) => (_jsx("div", { style: { height: itemHeight }, children: renderItem(item, startIndex + idx) }, startIndex + idx))) }) }) }));
}
