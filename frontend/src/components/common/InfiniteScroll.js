import React from "react";
import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useEffect, useRef } from 'react';
import { useIntersectionObserver } from '../../hooks/useIntersectionObserver';
/**
 * Infinite scroll component
 * Automatically loads more content when user scrolls near the bottom
 */
export const InfiniteScroll = ({ children, onLoadMore, hasMore, loading = false, threshold = 0.8, loader = _jsx("div", { className: "text-center py-4", children: "Loading..." }) }) => {
    const loadMoreRef = useRef(null);
    const isIntersecting = useIntersectionObserver(loadMoreRef, {
        threshold,
        rootMargin: '100px'
    });
    useEffect(() => {
        if (isIntersecting && hasMore && !loading) {
            onLoadMore();
        }
    }, [isIntersecting, hasMore, loading, onLoadMore]);
    return (_jsxs("div", { children: [children, hasMore && (_jsx("div", { ref: loadMoreRef, className: "load-more-trigger", children: loading && loader }))] }));
};
