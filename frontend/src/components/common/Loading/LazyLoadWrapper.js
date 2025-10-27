import { jsx as _jsx, Fragment as _Fragment } from "react/jsx-runtime";
import React, { Suspense } from 'react';
import { Spinner } from './Spinner';
export const LazyLoadWrapper = ({ children, fallback, minLoadTime = 0, }) => {
    const [isReady, setIsReady] = React.useState(minLoadTime === 0);
    React.useEffect(() => {
        if (minLoadTime > 0) {
            const timer = setTimeout(() => {
                setIsReady(true);
            }, minLoadTime);
            return () => clearTimeout(timer);
        }
    }, [minLoadTime]);
    const defaultFallback = (_jsx("div", { className: "lazy-load-placeholder", children: _jsx(Spinner, { size: "large" }) }));
    if (!isReady) {
        return _jsx(_Fragment, { children: fallback || defaultFallback });
    }
    return (_jsx(Suspense, { fallback: fallback || defaultFallback, children: children }));
};
